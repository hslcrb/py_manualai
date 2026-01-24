import os
import time
from database import DatabaseManager
from utils import highlight_text

class ManualEngine:
    def __init__(self, db_path=None):
        if db_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(os.path.dirname(current_dir), 'data', 'manual_ai.db')
        else:
            self.db_path = db_path
        
        # Load DB Manager (No loading time needed!)
        self.db = DatabaseManager(self.db_path)
        print(f"[ENGINE] Connected to High-Performance Database: {self.db_path}")

    def search(self, query):
        start_time = os.times()[4]
        query = query.strip()
        if not query: return None
        
        query_tokens = query.split()

        # 1. Exact Match [O(1) Hash Search (SQL Primary Key)]
        exact_res = self.db.get_exact_match(query)
        if exact_res:
            related = self.db.get_related_keywords(query_tokens)
            return {
                "response": exact_res,
                "type": "DIRECT_ANSWER",
                "strategy": "SQL_PRIMARY_KEY_LOOKUP",
                "confidence": 1.0,
                "time": os.times()[4] - start_time,
                "related": related
            }

        # 2. FTS Search (Full-Text Search Index)
        results, fts_time = self.db.search_fts(query)
        
        # UI Formatting
        formatted_results = []
        for res in results:
             # 하이라이팅 적용
            hl_title = highlight_text(res['title'], query_tokens)
            hl_content = highlight_text(res['content'], query_tokens)
            
            formatted_results.append({
                "title": hl_title,
                "content": hl_content,
                "score": res['score'], # FTS Rank
                "type": res['type'],
                "category": res['category']
            })
            
        elapsed_time = os.times()[4] - start_time
        related_kws = self.db.get_related_keywords(query_tokens)

        if formatted_results:
            response_text = f"검색 결과 {len(formatted_results)}건을 찾았습니다.\n"
            for res in formatted_results:
                source_tag = f"[{res['type']}/{res['category']}]"
                response_text += f"\n{source_tag} {res['title']}\n    {res['content'][:100]}..."
            
            if related_kws:
                response_text += f"\n\n[연관 검색어] {', '.join(related_kws)}"
                
            return {
                "response": response_text,
                "strategy": "SQL_FTS5_INDEX_SCAN",
                "confidence": 0.95, # FTS hit is high confidence
                "results": formatted_results,
                "related": related_kws,
                "time": elapsed_time
            }
            
        return {
            "response": f"검색어 '{query}'에 대한 결과를 찾지 못했습니다.\n추천 검색어: {', '.join(related_kws) if related_kws else '없음'}",
            "strategy": "FALLBACK",
            "confidence": 0.0,
            "time": elapsed_time
        }
