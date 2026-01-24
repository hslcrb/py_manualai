import json
import itertools
from collections import defaultdict, Counter
import time
import os
import random
from database import DatabaseManager

def migrate_to_sqlite():
    print("=====================================================================")
    print("   MANUAL AI v5.0 MIGRATION PROTOCOL (JSON -> SQLITE)   ")
    print("=====================================================================")
    
    # DB 초기화
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(os.path.dirname(current_dir), 'data', 'manual_ai.db')
    
    # 기존 DB 삭제 (Clean Start)
    if os.path.exists(db_path):
        os.remove(db_path)
        print("[INIT] Removed old database file.")
    
    db_manager = DatabaseManager(db_path)
    
    start_time = time.time()
    
    # === 데이터 생성 로직 (v4.0 Generator 재사용하여 Bulk Data 생성) ===
    # 메모리에 다 담는게 아니라, 배치 단위로 생성해서 DB에 넣어야 하지만
    # 현재 1.8만건 정도는 메모리 충분하므로 생성 후 Bulk Insert.
    
    topics = {
        "IT": ["파이썬", "자바", "리눅스", "윈도우", "맥북", "아이폰", "갤럭시", "AI", "블록체인", "클라우드", "서버", "해킹", "보안", "코딩", "개발자", "알고리즘"],
        "Health": ["다이어트", "비타민", "단백질", "헬스", "요가", "당뇨", "고혈압", "암", "스트레스", "수면", "영양제", "운동", "탈모", "피부관리"],
        "Finance": ["주식", "비트코인", "부동산", "적금", "청약", "환율", "금리", "재테크", "연말정산", "세금", "보험", "대출", "경제", "나스닥"],
        "Food": ["맛집", "레시피", "김치찌개", "파스타", "치킨", "피자", "커피", "디저트", "편의점", "다이어트식단", "배달", "떡볶이", "삼겹살", "라면"],
        "Entertain": ["넷플릭스", "영화", "드라마", "아이돌", "케이팝", "유튜브", "웹툰", "게임", "롤", "오버워치", "축구", "야구", "월드컵", "올림픽"],
        "Travel": ["제주도", "일본", "유럽", "미국", "호캉스", "캠핑", "글램핑", "비행기", "여권", "환전", "면세점", "부산", "강릉", "서울"]
    }
    
    doc_types = ["블로그", "뉴스", "카페", "지식백과", "쇼핑", "동영상"]
    title_templates = ["{topic} 정보", "{topic} 후기", "2026 {topic}", "{topic} 가이드", "{topic} 비밀", "{topic} TOP 10", "{topic} vs {comp}"]
    content_templates = ["{topic}에 대한 내용입니다. {comp}와 관련이 있습니다.", "사실 {topic}은 아주 훌륭합니다. {comp}보다 낫네요.", "{topic} 뉴스입니다."]

    docs_buffer = []
    exact_match_buffer = []
    related_buffer = []
    
    doc_id = 0
    entry_count = 0
    
    print("Generating Data Streams...")
    
    for category, keywords in topics.items():
        # A. 기본 문서
        for kw in keywords:
            doc = {
                "id": doc_id,
                "category": category,
                "type": "지식백과",
                "title": f"{kw}의 모든 것 - {category} 백과",
                "content": f"{kw}은(는) {category} 분야의 핵심 키워드입니다. 정의: {kw}란 무엇인가..."
            }
            docs_buffer.append(doc)
            exact_match_buffer.append((kw, doc['content']))
            doc_id += 1
            
        # B. 대량 증폭 (Massive Amplification)
        # 50,000건 생성 목표
        TARGET_PER_CAT = 8000 
        
        for _ in range(TARGET_PER_CAT):
            kw = random.choice(keywords)
            comp_kw = random.choice(keywords)
            doc_type = random.choice(doc_types)
            
            real_title = random.choice(title_templates).replace("{topic}", kw).replace("{comp}", comp_kw)
            real_content = random.choice(content_templates).format(topic=kw, comp=comp_kw)
            
            docs_buffer.append({
                "id": doc_id,
                "category": category,
                "type": doc_type,
                "title": real_title,
                "content": real_content
            })
            
            exact_match_buffer.append((real_title, real_content))
            
            if kw != comp_kw:
                related_buffer.append((kw, comp_kw, 1))
                related_buffer.append((comp_kw, kw, 1))
            
            doc_id += 1
            entry_count += 1
            
            if len(docs_buffer) >= 5000: # 5000개마다 커밋
                print(f"  > Flushing buffer ({doc_id} docs)...")
                db_manager.bulk_insert_documents(docs_buffer)
                docs_buffer = [] # Reset
                
    # 남은 버퍼 처리
    if docs_buffer:
        db_manager.bulk_insert_documents(docs_buffer)
        
    print(f"  > Inserting {len(exact_match_buffer)} Exact Matches...")
    # Exact Match 버퍼가 너무 크면 나눠서
    BATCH_SIZE = 10000
    for i in range(0, len(exact_match_buffer), BATCH_SIZE):
        batch = exact_match_buffer[i:i+BATCH_SIZE]
        db_manager.bulk_insert_exact_matches(batch)
        
    print(f"  > Inserting {len(related_buffer)} Related Keyword Relations...")
    # 중복 제거 및 집계 (파이썬 레벨에서 먼저)
    # 하지만 현재 구조상 그냥 DB에 때려넣고 중복은 무시(OR REPLACE)하거나,
    # 여기서는 간단히 그냥 넣음. 대략적인 통계만 필요하므로.
    for i in range(0, len(related_buffer), BATCH_SIZE):
        batch = related_buffer[i:i+BATCH_SIZE]
        db_manager.bulk_insert_related_keywords(batch)

    # 기본 채팅 데이터
    chat_patterns = [
        ("안녕", "안녕하세요! ManualAI v5.0 (SQLite Edition) 입니다."),
        ("버전", "현재 버전은 v5.0 - High Performance SQLite Engine 입니다."),
    ]
    db_manager.bulk_insert_exact_matches(chat_patterns)

    # 요약
    print(f"=====================================================================")
    print(f"   MIGRATION COMPLETE")
    print(f"   - Total Documents: {doc_id:,}")
    print(f"   - Database: {db_path}")
    print(f"   - Engine: SQLite FTS5 (Trigram)")
    print(f"   - Time Elapsed: {time.time() - start_time:.2f}s")
    print(f"=====================================================================")

if __name__ == "__main__":
    migrate_to_sqlite()
