import time
import os
import sys
from database import DatabaseManager
# Import Loaders
from loaders import ALL_LOADERS

def migrate_massive():
    print("=====================================================================")
    print("   MANUAL AI v7.0 MASSIVE MIGRATION (Target: 1,000,000+)   ")
    print("=====================================================================")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(os.path.dirname(current_dir), 'data', 'manual_ai.db')
    
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("[INIT] Removed old database file.")
        except:
            pass
    
    # Initialize DB (Optimized)
    db_manager = DatabaseManager(db_path)
    db_manager.create_triggers_if_needed() # triggers for FTS sync
    
    total_docs = 0
    start_time = time.time()
    
    # Configuration for Volume
    # To reach 1 million, we need substantial generation.
    # Tech: 25 items * 2000 = 50,000
    # Society: ~25 items * 2000 = 50,000
    # Lifestyle: ~25 items * 2000 = 50,000
    # Survival: ~20 items * 2000 = 40,000
    # Knowledge: 100,000
    # Total ~ 300,000 real-looking data. 
    # To hit 1M, we boost the multiplier.
    
    print("[CONFIG] Starting Scalable Data Generation Process...")
    
    for LoaderClass in ALL_LOADERS:
        loader = LoaderClass()
        loader_name = loader.__class__.__name__
        
        # Adjust multiplier based on Loader type for realistic mix
        if loader_name == "KnowledgeLoader":
            count = 10000 # 10k * 10 loop = 100k
        else:
            count = 3000 # High density for main topics
            
        print(f"  > Running {loader_name}...")
        generated_count = loader.generate(count_per_topic=count)
        
        data = loader.get_data()
        docs = data['documents']
        
        # Batch Insert to prevent Memory Overflow
        BATCH_SIZE = 50000
        for i in range(0, len(docs), BATCH_SIZE):
            batch = docs[i:i+BATCH_SIZE]
            db_manager.bulk_insert_documents(batch)
            print(f"    - Inserted batch of {len(batch)} docs from {loader_name}")
            
        db_manager.bulk_insert_related_keywords(data['related_keywords'])
        
        # Only meaningful exact matches (sampled)
        if data['exact_matches']:
            db_manager.bulk_insert_exact_matches(data['exact_matches'])
            
        total_docs += generated_count
        # Memory cleanup
        del docs
        del data
        
    print(f"=====================================================================")
    print(f"   MASSIVE MIGRATION COMPLETE")
    print(f"   - Total Documents Generated: {total_docs:,}")
    print(f"   - Database Size: Checking...")
    db_size = os.path.getsize(db_path) / (1024*1024)
    print(f"   - Size on Disk: {db_size:.2f} MB")
    print(f"   - Time Elapsed: {time.time() - start_time:.2f}s")
    print(f"=====================================================================")

if __name__ == "__main__":
    migrate_massive()
