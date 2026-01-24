import json
import itertools
from collections import defaultdict, Counter
import time
import os
import random
from database import DatabaseManager

def migrate_to_sqlite_tree():
    print("=====================================================================")
    print("   MANUAL AI v6.0 TREE-STRUCTURE MIGRATION (100K+ TARGET)   ")
    print("=====================================================================")
    
    # DB 초기화
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(os.path.dirname(current_dir), 'data', 'manual_ai.db')
    
    if os.path.exists(db_path):
        os.remove(db_path)
        print("[INIT] Removed old database file.")
    
    db_manager = DatabaseManager(db_path)
    start_time = time.time()
    
    # === 계층적 트리 구조 데이터 정의 (Hierarchical Tree Data) ===
    # 대주제(Root) -> 중주제(Middle) -> 소주제(Small) -> 미시주제(Micro)
    
    topic_tree = {
        "기술(Technology)": {
            "소프트웨어": {
                "프로그래밍 언어": ["파이썬", "자바", "C++", "자바스크립트", "러스트", "Go"],
                "운영체제": ["리눅스", "윈도우", "MacOS", "우분투", "안드로이드"],
                "데이터베이스": ["MySQL", "PostgreSQL", "SQLite", "MongoDB", "Redis"]
            },
            "하드웨어": {
                "컴퓨터 부품": ["CPU", "GPU", "RAM", "SSD", "메인보드", "파워서플라이"],
                "모바일": ["스마트폰", "태블릿", "워치", "폴더블폰"],
                "반도체": ["메모리", "시스템반도체", "파운드리", "ASML", "EUV"]
            }
        },
        "사회(Society)": {
            "경제": {
                "주식": ["나스닥", "코스피", "ETF", "배당주", "테마주", "공매도"],
                "암호화폐": ["비트코인", "이더리움", "리플", "도지코인", "디파이", "NFT"],
                "부동산": ["아파트", "청약", "LTV", "DSR", "전세", "월세"]
            },
            "문화": {
                "영화": ["마블", "아바타", "독립영화", "OTT", "넷플릭스", "티빙"],
                "음악": ["K-POP", "발라드", "힙합", "클래식", "재즈", "인디"],
                "여행": ["국내여행", "해외여행", "유럽투어", "동남아", "호캉스", "캠핑"]
            }
        },
        "생활(Life)": {
            "건강": {
                "운동": ["헬스", "요가", "필라테스", "크로스핏", "러닝", "등산"],
                "식단": ["저탄고지", "채식", "간헐적단식", "단백질", "비타민"],
                "질병": ["감기", "코로나", "당뇨", "고혈압", "우울증", "불면증"]
            },
            "음식": {
                "한식": ["김치찌개", "불고기", "비빔밥", "삼겹살", "떡볶이"],
                "양식": ["파스타", "스테이크", "피자", "리조또", "샐러드"],
                "디저트": ["커피", "케이크", "마카롱", "빙수", "와플"]
            }
        }
    }
    
    doc_types = ["[지식백과]", "[전문가 칼럼]", "[뉴스 속보]", "[블로그 리뷰]", "[커뮤니티]", "[Q&A]"]
    
    # 템플릿 고도화
    templates = {
        "title": [
            "{micro}의 모든 것: {small} 분야 완벽 가이드",
            "2026년 {micro} 트렌드 전망 및 분석",
            "{micro}, 과연 지금 시작해도 늦지 않았을까?",
            "전문가가 말하는 {micro}의 3가지 비밀",
            "당신이 몰랐던 {middle} - {micro} 의 진실",
            "{small} 분야의 혁신: {micro} 심층 리포트",
            "초보자를 위한 {micro} 입문서 (EP.1)",
            "{micro} vs {comp}: 승자는 누구인가?",
            "실시간 {micro} 이슈 정리",
            "{micro} 관련주 TOP 5 정리"
        ],
        "content_intro": [
            "{root} 분야에서 가장 핫한 키워드는 바로 '{micro}'입니다. ",
            "안녕하세요. 오늘은 {small} 카테고리의 핵심인 '{micro}'에 대해 알아봅니다. ",
            "최근 '{micro}'에 대한 관심이 급증하고 있습니다. 특히 {comp}와의 비교가 화제인데요. ",
            "속보입니다. {middle} 시장에서 '{micro}'가 차지하는 비중이 역대 최고치를 기록했습니다. "
        ],
        "content_body": [
            "{micro}의 장점은 접근성이 좋다는 것입니다. 하지만 {comp}와 비교했을 때 비용 문제가 있을 수 있습니다. ",
            "전문가들은 {micro}의 미래를 매우 긍정적으로 보고 있습니다. 특히 {small} 생태계와의 시너지가 기대됩니다. ",
            "저도 직접 {micro}을(를) 경험해봤는데요. {middle} 전체를 관통하는 인사이트를 얻을 수 있었습니다. ",
            "데이터에 따르면 {micro} 검색량이 전년 대비 300% 증가했습니다. 이는 {root} 전반의 트렌드 변화를 의미합니다. "
        ],
        "content_concl": [
            "결론적으로 {micro}은(는) 필수적인 요소가 될 것입니다. 더 자세한 내용은 {small} 백서를 참고하세요.",
            "지금 바로 {micro}에 대해 공부해보세요. {comp}보다 더 큰 기회가 있을 수 있습니다.",
            "다음 시간에는 {comp}에 대해 더 깊이 다뤄보겠습니다. {micro} 리포트를 마칩니다."
        ]
    }

    docs_buffer = []
    related_buffer = []
    
    doc_id = 0
    total_generated = 0
    
    print("Generating HIERARCHICAL TREE Data Stream...")
    
    # 재귀적 탐색 대신, 명시적 4중 루프로 구조화 (Root->Middle->Small->Micro)
    for root, middles in topic_tree.items():
        print(f"  > Processing Root: {root}")
        for middle, smalls in middles.items():
            for small, micros in smalls.items():
                
                # 같은 소주제 내에서 비교 키워드 추출용 리스트
                siblings = micros
                
                for micro in micros:
                    # 각 미시주제(Micro)마다 대량의 문서 생성
                    # 목표: 총 10만개. 
                    # 현재 마이크로 주제 개수 대략 60~70개.
                    # 각 주제당 약 1500~2000개 문서 생성 필요.
                    
                    TARGET_DOCS_PER_MICRO = 1500
                    
                    for _ in range(TARGET_DOCS_PER_MICRO):
                        comp = random.choice(siblings) # 비교 대상
                        dtype = random.choice(doc_types)
                        
                        # 템플릿 조합
                        t_tmpl = random.choice(templates["title"])
                        c_intro = random.choice(templates["content_intro"])
                        c_body = random.choice(templates["content_body"])
                        c_concl = random.choice(templates["content_concl"])
                        
                        real_title = t_tmpl.format(root=root, middle=middle, small=small, micro=micro, comp=comp)
                        real_content = (c_intro + c_body + c_concl).format(root=root, middle=middle, small=small, micro=micro, comp=comp)
                        
                        # 태그 생성 (계층 구조 반영)
                        tags = f"{root} > {middle} > {small}"
                        
                        # 버퍼 저장
                        docs_buffer.append({
                            "id": doc_id,
                            "category": tags, # 카테고리에 '대>중>소' 계층 정보 저장
                            "type": dtype,
                            "title": real_title,
                            "content": real_content
                        })
                        
                        # 연관 검색어 (같은 그룹 내 키워드끼리)
                        if micro != comp:
                            related_buffer.append((micro, comp, 1))
                        
                        doc_id += 1
                        total_generated += 1
                        
                        # DB Flush (5000개 단위)
                        if len(docs_buffer) >= 5000:
                            db_manager.bulk_insert_documents(docs_buffer)
                            print(f"    [Flush] {total_generated} docs generated. (Current: {micro})")
                            docs_buffer = []

    # 남은 버퍼 처리
    if docs_buffer:
        db_manager.bulk_insert_documents(docs_buffer)
        
    print(f"  > Inserting {len(related_buffer)} Related Keywords...")
    BATCH_SIZE = 10000
    for i in range(0, len(related_buffer), BATCH_SIZE):
        batch = related_buffer[i:i+BATCH_SIZE]
        db_manager.bulk_insert_related_keywords(batch)

    # 기본 대화 데이터 추가
    chat_patterns = [
        ("안녕", "안녕하세요! ManualAI v6.0 (Tree Structure Edition) 입니다."),
        ("매뉴얼", "현재 데이터베이스는 대>중>소>미시 주제로 완벽하게 구조화되어 있습니다."),
        ("규모", f"현재 약 {doc_id:,}개의 계층형 문서가 인덱싱되어 있습니다.")
    ]
    db_manager.bulk_insert_exact_matches(chat_patterns)

    # 요약
    print(f"=====================================================================")
    print(f"   MIGRATION COMPLETE (v6.0)")
    print(f"   - Total Documents: {doc_id:,}")
    print(f"   - Architecture: Hierarchical Tree (Root/Middle/Small/Micro)")
    print(f"   - Engine: SQLite FTS5")
    print(f"   - Time Elapsed: {time.time() - start_time:.2f}s")
    print(f"=====================================================================")

if __name__ == "__main__":
    migrate_to_sqlite_tree()
