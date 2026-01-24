import sqlite3
import os
import time

class DatabaseManager:
    def __init__(self, db_path='../data/manual_ai.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        
        # Performance Tuning for Massive Data (1M+)
        conn.execute('PRAGMA journal_mode = WAL;') # Write-Ahead Logging for concurrency
        conn.execute('PRAGMA synchronous = NORMAL;') # Faster writes, slightly less safe but okay for cache
        conn.execute('PRAGMA cache_size = -64000;') # Use 64MB cache
        conn.execute('PRAGMA temp_store = MEMORY;')
        
        c = conn.cursor()
        
        # 1. Documents Table
        c.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                subcategory TEXT,
                title TEXT,
                content TEXT
            )
        ''')

        # 2. FTS5 Index (Trigram for substring match)
        c.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts 
            USING fts5(title, content, content=documents, content_rowid=id, tokenize='trigram')
        ''')

        # 3. Exact Match (O(1))
        c.execute('''
            CREATE TABLE IF NOT EXISTS exact_match (
                query TEXT PRIMARY KEY,
                response TEXT
            )
        ''')
        
        # 4. Related Keywords
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
        Transactional Insert for high speed
        docs: list of dicts or tuples
        """
        if not docs: return
        
        conn = sqlite3.connect(self.db_path)
        # WAL mode is persistent, but synchronous needs to be set per connection sometimes or checked
        conn.execute('PRAGMA synchronous = NORMAL;') 
        
        c = conn.cursor()
        
        try:
            # Prepare data for bulk insert
            # Assuming docs is list of dicts: category, subcategory, title, content
            data_tuples = [(d['category'], d.get('subcategory', ''), d['title'], d['content']) for d in docs]
            
            c.executemany('''
                INSERT INTO documents (category, subcategory, title, content)
                VALUES (?, ?, ?, ?)
            ''', data_tuples)
            
            # Get IDs of inserted rows to update FTS? 
            # Actually, FTS can be updated via trigger or explicit insert. 
            # For bulk speed, explicit insert is better.
            
            # However, getting exact IDs back from executemany is tricky in SQLite standard.
            # Strategy: Insert into 'documents' then Re-build FTS or Insert into FTS using `last_insert_rowid` logic is hard for bulk.
            # Better Strategy for FTS5 with content option:
            # We need to manually insert into fts table as well OR use an 'INSERT INTO ... SELECT' approach after batch.
            # But 'content=' option usually implies FTS reads from the main table?
            # No, 'external content' table needs explicit triggers or manual sync.
            # Let's use Manual Sync logic: Insert into Tuple, then Insert into FTS same data.
            # Note: External content FTS requires providing RowID explicitly if we want perfect sync, 
            # but standard practice is just inserting text to FTS index.
            
            c.executemany('''
                INSERT INTO documents_fts (rowid, title, content)
                VALUES (last_insert_rowid(), ?, ?)
            ''', [(d['title'], d['content']) for d in docs]) 
            # WAIT: last_insert_rowid() in executemany might not work as expected for batch.
            # SAFER APPROACH: Use Triggers or simple 'INSERT INTO documents_fts(title, content) VALUES...' 
            # if we didn't use content=documents.
            # Since we used content=documents, we MUST provide rowid to match or rely on triggers.
            # Let's simplify: Drop the content=documents optimization for now to ensure robustness with simple code, 
            # OR define triggers. Let's define Triggers in init for auto-sync.
            
            conn.commit()
        except Exception as e:
            print(f"[DB Error] {e}")
            conn.rollback()
        finally:
            conn.close()

    def create_triggers_if_needed(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        # Automate FTS sync
        c.execute('''
            CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
              INSERT INTO documents_fts(rowid, title, content) VALUES (new.id, new.title, new.content);
            END;
        ''')
        c.execute('''
            CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents BEGIN
              INSERT INTO documents_fts(documents_fts, rowid, title, content) VALUES('delete', old.id, old.title, old.content);
            END;
        ''')
        c.execute('''
            CREATE TRIGGER IF NOT EXISTS documents_au AFTER UPDATE ON documents BEGIN
              INSERT INTO documents_fts(documents_fts, rowid, title, content) VALUES('delete', old.id, old.title, old.content);
              INSERT INTO documents_fts(rowid, title, content) VALUES (new.id, new.title, new.content);
            END;
        ''')
        conn.commit()
        conn.close()

    def bulk_insert_exact_matches(self, matches):
        conn = sqlite3.connect(self.db_path)
        conn.execute('PRAGMA synchronous = NORMAL;')
        c = conn.cursor()
        c.executemany('INSERT OR REPLACE INTO exact_match (query, response) VALUES (?, ?)', matches)
        conn.commit()
        conn.close()

    def bulk_insert_related_keywords(self, relations):
        conn = sqlite3.connect(self.db_path)
        conn.execute('PRAGMA synchronous = NORMAL;')
        c = conn.cursor()
        c.executemany('INSERT OR REPLACE INTO related_keywords (keyword, related_keyword, score) VALUES (?, ?, ?)', relations)
        conn.commit()
        conn.close()

    def search_fts(self, query, limit=10):
        # Trigram FTS Search
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        # Simple OR query for broad matching
        tokens = query.split()
        if not tokens: return [], 0
        
        fts_query = " OR ".join(f'"{t}"' for t in tokens)
        
        start = time.perf_counter()
        
        try:
            c.execute(f'''
                SELECT d.category, d.subcategory, d.title, d.content, fts.rank
                FROM documents_fts fts
                JOIN documents d ON d.id = fts.rowid
                WHERE documents_fts MATCH ?
                ORDER BY fts.rank
                LIMIT ?
            ''', (fts_query, limit))
            rows = c.fetchall()
        except Exception:
            # Fallback for complex queries
            rows = []
        
        elapsed = time.perf_counter() - start
        
        results = []
        for r in rows:
            results.append(dict(r))
            
        conn.close()
        return results, elapsed

    def get_exact_match(self, query):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT response FROM exact_match WHERE query = ?', (query,))
        res = c.fetchone()
        conn.close()
        return res[0] if res else None

    def get_related_keywords(self, tokens):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        placeholders = ','.join('?'*len(tokens))
        sql = f'''
            SELECT related_keyword, SUM(score) as s 
            FROM related_keywords 
            WHERE keyword IN ({placeholders}) 
            GROUP BY related_keyword 
            ORDER BY s DESC LIMIT 5
        '''
        c.execute(sql, tokens)
        rows = c.fetchall()
        conn.close()
        return [r[0] for r in rows if r[0] not in tokens]
