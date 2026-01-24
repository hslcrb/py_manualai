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
        
        self.db = DatabaseManager(self.db_path)
        print(f"[ENGINE] Connected to High-Performance Database: {self.db_path}")

    def search(self, query):
        start_time = os.times()[4]
        query = query.strip()
        if not query: return None
        
        query_tokens = query.split()

        # 1. Primary AI Response (Gemini/Google Style "Featured Snippet")
        # Exact match or first direct fact found
        ai_response = None
        exact_res = self.db.get_exact_match(query)
        if exact_res:
            ai_response = exact_res
            strategy = "DIRECT_INTEL"
        else:
            # Check if query tokens match any high-levelMicro items for a quick summary
            # We use an internal heuristic or just rely on FTS ranking for now.
            strategy = "SEARCH_INDEX_SCAN"

        # 2. Advanced Search Results (Portal Style)
        # Fetch 30 results internally but show Top 5 (for diversity/relevance)
        raw_results, fts_time = self.db.search_fts(query, limit=30)
        
        # 3. Intelligent Ranking & Formatting
        formatted_results = []
        seen_contents = set() # For diversity (prevent repetitive templates)
        
        for res in raw_results:
            if len(formatted_results) >= 5: break
            
            # Content Hash (Simplified) for De-duplication
            content_snippet = res['content'][:50]
            if content_snippet in seen_contents: continue
            seen_contents.add(content_snippet)
            
            hl_title = highlight_text(res['title'], query_tokens)
            hl_content = highlight_text(res['content'], query_tokens)
            
            formatted_results.append({
                "title": hl_title,
                "content": hl_content,
                "rank": res.get('rank', 0),
                "type": res.get('subcategory', 'General'),
                "category": res.get('category', 'Unknown')
            })
            
        # If no exact match but we have a result, use the top result as a 'hint' or summary
        if not ai_response and formatted_results:
            ai_response = formatted_results[0]['content']

        elapsed_time = os.times()[4] - start_time
        related_kws = self.db.get_related_keywords(query_tokens)

        return {
            "ai_response": ai_response or "찾으시는 정보가 데이터베이스에 존재하지 않습니다.",
            "search_results": formatted_results,
            "strategy": strategy,
            "confidence": 0.98 if exact_res else 0.85,
            "related": related_kws,
            "time": elapsed_time
        }
