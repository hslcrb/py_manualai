import sqlite3
import os
import json
import time

class DatabaseManager:
    def __init__(self, db_path='../data/manual_ai.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        # 데이터 디렉토리 생성
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # 1. 문서 테이블 (실제 데이터 저장)
        # category 컬럼 추가
        c.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                category TEXT,
                type TEXT,
                title TEXT,
                content TEXT
            )
        ''')

        # 2. FTS5 (Full-Text Search) 가상 테이블 생성
        # 구글처럼 고속 텍스트 검색을 위한 특수 테이블
        # N-gram 토크나이저를 사용하여 부분 문자열 검색 지원 (trigram 권장)
        c.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts 
            USING fts5(title, content, content=documents, content_rowid=id, tokenize='trigram')
        ''')

        # 3. 정확 매칭용 키-값 테이블 (채팅용, O(1) 속도)
        c.execute('''
            CREATE TABLE IF NOT EXISTS exact_match (
                query TEXT PRIMARY KEY,
                response TEXT
            )
        ''')
        
        # 4. 연관 검색어 테이블 (Relational)
        c.execute('''
            CREATE TABLE IF NOT EXISTS related_keywords (
                keyword TEXT,
                related_keyword TEXT,
                score INTEGER,
                PRIMARY KEY (keyword, related_keyword)
            )
        ''')

        conn.commit()
        conn.close()

    def bulk_insert_documents(self, docs):
        """
        대용량 제네레이터 데이터를 한 번에 넣기 (Transaction 사용)
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        try:
            # 1. Main Data
            c.executemany('''
                INSERT OR REPLACE INTO documents (id, category, type, title, content)
                VALUES (:id, :category, :type, :title, :content)
            ''', docs)
            
            # 2. FTS Index Update
            # FTS 테이블에는 ID와 텍스트만 넣으면 됨 (자동 인덱싱)
            c.executemany('''
                INSERT OR REPLACE INTO documents_fts (rowid, title, content)
                VALUES (:id, :title, :content)
            ''', docs)
            
            conn.commit()
            print(f"[DB] Successfully inserted {len(docs)} documents.")
        except Exception as e:
            print(f"[DB] Error inserting documents: {e}")
            conn.rollback()
        finally:
            conn.close()

    def bulk_insert_exact_matches(self, matches):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.executemany('INSERT OR REPLACE INTO exact_match (query, response) VALUES (?, ?)', matches)
        conn.commit()
        conn.close()
        
    def bulk_insert_related_keywords(self, relations):
        # relations: [(kw, related_kw, score), ...]
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.executemany('INSERT OR REPLACE INTO related_keywords (keyword, related_keyword, score) VALUES (?, ?, ?)', relations)
        conn.commit()
        conn.close()

    def search_fts(self, query):
        """
        FTS5 고속 전문 검색 수행
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        # SQLite FTS 쿼리 문법으로 변환 (AND 검색 혹은 OR 검색)
        # "파이썬 다이어트" -> "파이썬 OR 다이어트"
        fts_query = " OR ".join(f'"{token}"' for token in query.split())
        
        start = time.perf_counter()
        
        # bm25() 함수는 SQLite 최신 버전에서 기본 제공하거나 사용자 정의 필요. 
        # 여기서는 rank 기본 기능을 사용 (간단한 매칭 점수)
        c.execute(f'''
            SELECT d.category, d.type, d.title, d.content, fts.rank
            FROM documents_fts fts
            JOIN documents d ON d.id = fts.rowid
            WHERE documents_fts MATCH ?
            ORDER BY fts.rank
            LIMIT 5
        ''', (fts_query,))
        
        rows = c.fetchall()
        elapsed = time.perf_counter() - start
        
        results = []
        for row in rows:
            results.append({
                "category": row['category'],
                "type": row['type'],
                "title": row['title'],
                "content": row['content'],
                "score": row['rank'] # FTS rank는 낮을수록(음수) 좋거나 구현따라 다름. 보통 matchinfo 사용 필요하나 여기선 기본사용.
            })
            
        conn.close()
        return results, elapsed

    def get_exact_match(self, query):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT response FROM exact_match WHERE query = ?', (query,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

    def get_related_keywords(self, query_tokens):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        placeholders = ','.join(['?'] * len(query_tokens))
        sql = f'''
            SELECT related_keyword, SUM(score) as total_score 
            FROM related_keywords 
            WHERE keyword IN ({placeholders})
            GROUP BY related_keyword 
            ORDER BY total_score DESC 
            LIMIT 5
        '''
        
        c.execute(sql, query_tokens)
        rows = c.fetchall()
        
        conn.close()
        
        related = [row[0] for row in rows if row[0] not in query_tokens]
        return related
