import json
import os
import time
from collections import defaultdict
from utils import get_ngrams, calculate_similarity_score, highlight_text
from bm25 import BM25

class ManualEngine:
    def __init__(self, db_path=None):
        if db_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(os.path.dirname(current_dir), 'data', 'manual_db.json')
        else:
            self.db_path = db_path
        
        self.db = None
        self.bm25_ranker = None
        self.load_db()

    def load_db(self):
        print(f"[ENGINE] Loading Knowledge Base from {self.db_path}...")
        start_time = time.time()
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                self.db = json.load(f)
            
            print("[ENGINE] Initializing BM25 Ranking Algorithm...")
            # 문서를 토큰화하여 BM25에 주입
            corpus = [doc['keywords'] for doc in self.db['documents']]
            self.bm25_ranker = BM25(corpus)
            
            print(f"[ENGINE] Database Loaded in {time.time() - start_time:.4f}s.")
            print(f"         Total Documents: {self.db['meta']['total_documents']:,}")
            print(f"         Total Entries: {self.db['meta']['total_entries']:,}")
        
        except FileNotFoundError:
            print("[ENGINE] ERROR: Database file not found!")
            self.db = {"exact_match": {}, "documents": [], "related_keywords": {}}

    def search(self, query):
        start_time = os.times()[4]
        query = query.strip()
        if not query: return None
        
        query_tokens = query.split()

        # 1. Exact Match [O(1)] - 채팅형 쿼리 우선
        if query in self.db["exact_match"]:
            return {
                "response": self.db["exact_match"][query][0],
                "type": "DIRECT_ANSWER",
                "strategy": "EXACT_MATCH",
                "confidence": 1.0,
                "time": os.times()[4] - start_time,
                "related": self._get_related_keywords(query_tokens)
            }

        # 2. Portal Search (BM25)
        top_docs_indices = self.bm25_ranker.get_top_n(query_tokens, n=5) # Top 5 결과
        
        results = []
        best_score = 0.0
        
        if top_docs_indices:
            best_score = top_docs_indices[0][1]
            
            for doc_idx, score in top_docs_indices:
                doc = self.db['documents'][doc_idx]
                
                # 하이라이팅 적용
                hl_title = highlight_text(doc['title'], query_tokens)
                hl_content = highlight_text(doc['content'], query_tokens)
                
                results.append({
                    "title": hl_title,
                    "content": hl_content,
                    "score": score,
                    "type": doc['type'],
                    "category": doc.get('category', 'General')
                })
                
        elapsed_time = os.times()[4] - start_time
        related_kws = self._get_related_keywords(query_tokens)

        if results and best_score > 0.5:
            # 검색 결과 포맷팅 (포털 스타일)
            response_text = f"검색 결과 {len(results)}건을 찾았습니다.\n"
            for i, res in enumerate(results):
                # UI 포맷팅
                source_tag = f"[{res['type']}/{res['category']}]"
                response_text += f"\n{source_tag} {res['title']} (유사도: {res['score']:.2f})\n    {res['content'][:100]}..."
            
            if related_kws:
                response_text += f"\n\n[연관 검색어] {', '.join(related_kws)}"
                
            return {
                "response": response_text,
                "strategy": "BM25_RANKING_SEARCH",
                "confidence": best_score,
                "results": results,
                "related": related_kws,
                "time": elapsed_time
            }
            
        return {
            "response": f"검색어 '{query}'에 대한 정확한 결과를 찾지 못했습니다.\n추천 검색어: {', '.join(related_kws) if related_kws else '없음'}",
            "strategy": "FALLBACK",
            "confidence": 0.0,
            "time": elapsed_time
        }

    def _get_related_keywords(self, query_tokens):
        """
        쿼리 토큰 중 하나라도 관련된 키워드가 있으면 반환
        """
        related = set()
        for token in query_tokens:
            if token in self.db.get("related_keywords", {}):
                related.update(self.db["related_keywords"][token])
        
        # 본인 제외
        for token in query_tokens:
            if token in related:
                related.remove(token)
                
        return list(related)[:5]
