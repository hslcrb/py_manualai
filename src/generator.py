import json
import itertools
from collections import defaultdict, Counter
import time
import os
import random
from utils import get_ngrams

def generate_manual_db():
    print("=====================================================================")
    print("   GENERATE MANUAL AI DATABASE v4.0 (HYPER-SCALE PORTAL EDITION)   ")
    print("=====================================================================")
    
    start_time = time.time()
    
    # === 1. 어휘 및 토픽 데이터베이스 (Lexical Database) ===
    # 포털급 데이터를 위한 방대한 어휘 풀
    topics = {
        "IT": ["파이썬", "자바", "리눅스", "윈도우", "맥북", "아이폰", "갤럭시", "AI", "블록체인", "클라우드", "서버", "해킹", "보안", "코딩", "개발자", "알고리즘"],
        "Health": ["다이어트", "비타민", "단백질", "헬스", "요가", "당뇨", "고혈압", "암", "스트레스", "수면", "영양제", "운동", "탈모", "피부관리"],
        "Finance": ["주식", "비트코인", "부동산", "적금", "청약", "환율", "금리", "재테크", "연말정산", "세금", "보험", "대출", "경제", "나스닥"],
        "Food": ["맛집", "레시피", "김치찌개", "파스타", "치킨", "피자", "커피", "디저트", "편의점", "다이어트식단", "배달", "떡볶이", "삼겹살", "라면"],
        "Entertain": ["넷플릭스", "영화", "드라마", "아이돌", "케이팝", "유튜브", "웹툰", "게임", "롤", "오버워치", "축구", "야구", "월드컵", "올림픽"],
        "Travel": ["제주도", "일본", "유럽", "미국", "호캉스", "캠핑", "글램핑", "비행기", "여권", "환전", "면세점", "부산", "강릉", "서울"]
    }
    
    doc_types = ["블로그", "뉴스", "카페", "지식백과", "쇼핑", "동영상"]
    
    # 템플릿: 제목 생성용
    title_templates = [
        "{topic} 관련 필수 정보 정리",
        "{topic} 진짜 좋을까? 솔직 후기",
        "2026년 {topic} 트렌드 분석",
        "{topic} 초보자를 위한 완벽 가이드",
        "당신이 몰랐던 {topic}의 비밀",
        "{topic} 추천 TOP 10",
        "{topic} vs {topic_comp} 비교 분석",
        "오늘의 {topic} 뉴스 요약",
        "{topic} 구매 전 꼭 봐야할 글",
        "제대로 된 {topic} 찾는 법"
    ]
    
    # 템플릿: 내용 생성용
    content_templates = [
        "안녕하세요. 오늘은 {topic}에 대해 알아보겠습니다. 최근 많은 분들이 {topic}에 관심을 가지고 계신데요. 특히 {related}와 관련된 이슈가 화제입니다. 결론적으로 말씀드리면 {topic}은 매우 중요합니다.",
        "{topic} 관련 정보를 찾고 계신가요? 제가 직접 경험해본 {topic} 후기를 공유합니다. 장점은 {adj1}하고, 단점은 {adj2}하다는 것입니다. 자세한 내용은 본문을 참고하세요.",
        "속보입니다. {topic} 시장이 급변하고 있습니다. 전문가들은 {topic}의 미래를 {adj1}하게 전망하고 있습니다. 관련주 및 투자 포인트에 대해 분석해 봅니다.",
        "이번 영상에서는 {topic} 꿀팁을 대방출합니다. {topic} 잘하는 법, {topic} 싸게 사는 법 등 다양한 노하우를 담았습니다. 구독과 좋아요 부탁드립니다."
    ]
    
    adjectives = ["놀라운", "충격적인", "혁신적인", "위험한", "안전한", "저렴한", "비싼", "최고의", "최악의", "신기한"]
    
    database = {
        "meta": {
            "version": "4.0 (Hyperscale)",
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_entries": 0,
            "total_documents": 0,
        },
        "exact_match": {}, 
        "documents": [],
        "related_keywords": defaultdict(Counter) # 연관 검색어용 (단어 -> 연관단어 카운트)
    }

    doc_id = 0
    entry_count = 0

    # === 2. 매시브 데이터 생성 (Massive Data Generation) ===
    # 각 토픽별로 대량의 문서 생성
    
    print("Generating Hyper-scale Knowledge Graph...")
    
    for category, keywords in topics.items():
        print(f"  > Processing Category: {category} ({len(keywords)} base keywords)")
        
        # 키워드 조합 생성 (Pairing)
        pairs = list(itertools.permutations(keywords, 2))
        
        # 1. 문서 대량 생성 (토픽당 1000개 이상 목표)
        # 키워드 기반 + 랜덤 조합
        
        # A. 기본 키워드 문서
        for kw in keywords:
            # 토픽 대표 문서
            title = f"{kw}의 모든 것 - {category} 백과"
            content = f"{kw}은(는) {category} 분야의 핵심 키워드입니다. 정의: {kw}란 무엇인가..."
            
            doc = {
                "id": doc_id,
                "category": category,
                "type": "지식백과",
                "title": title,
                "content": content,
                "keywords": [kw, category, "정보", "정의"]
            }
            database["documents"].append(doc)
            database["exact_match"][kw] = [content] # 정확히 키워드만 쳤을 때
            doc_id += 1
            entry_count += 1
            
        # B. 조합형/변형형 문서 (Volume Amplification)
        # 생성할 문서 수 설정 (카테고리당 약 3000개~5000개)
        TARGET_DOCS_PER_CAT = 3000
        
        for _ in range(TARGET_DOCS_PER_CAT):
            kw = random.choice(keywords)
            comp_kw = random.choice(keywords)
            doc_type = random.choice(doc_types)
            tmpl_t = random.choice(title_templates)
            tmpl_c = random.choice(content_templates)
            adj1 = random.choice(adjectives)
            adj2 = random.choice(adjectives)
            
            # 제목/내용 생성
            real_title = tmpl_t.replace("{topic}", kw).replace("{topic_comp}", comp_kw)
            real_content = tmpl_c.format(topic=kw, related=comp_kw, adj1=adj1, adj2=adj2)
            
            # 태그/키워드 추출 (연관 검색어 학습용)
            doc_kws = [kw, category, doc_type, comp_kw]
            if kw != comp_kw:
                # 동시 출현 단어 기록 (연관 검색어 로직)
                database["related_keywords"][kw][comp_kw] += 1
                database["related_keywords"][comp_kw][kw] += 1
            
            doc = {
                "id": doc_id,
                "category": category,
                "type": doc_type,
                "title": real_title,
                "content": real_content,
                "keywords": doc_kws
            }
            database["documents"].append(doc)
            
            # 정확 일치 쿼리 추가 (제목 그대로 검색시)
            database["exact_match"][real_title] = [real_content]
            
            doc_id += 1
            entry_count += 1

    # === 3. 대화형 데이터 주입 (Chat Data Injection) ===
    # 기존 대화 로직 유지 + 확장
    print("  > Injecting Conversational Logic...")
    chat_patterns = [
        ("안녕", "안녕하세요! ManualAI v4.0 포털 엔진입니다."),
        ("날씨", "현재 시스템상 외부 날씨 정보에 접근할 수 없으나, 기상청 검색 결과를 보여드릴까요?"),
        ("심심해", "재미있는 '유머'나 '게임'을 검색해보시는 건 어떨까요?"),
        ("배고파", "맛집 카테고리에서 '김치찌개'나 '치킨'을 검색해보세요!"),
        ("주식 추천", "저는 투자를 권유하지 않습니다. 대신 '삼성전자'나 '나스닥' 관련 뉴스를 검색해드릴 수 있습니다.")
    ]
    
    for q, r in chat_patterns:
        database["exact_match"][q] = [r]
        entry_count += 1

    # 최종 메타데이터 업데이트
    database["meta"]["total_entries"] = entry_count
    database["meta"]["total_documents"] = doc_id
    
    # 연관 검색어 최적화 (Counter 객체를 리스트로 변환하여 json 직렬화 가능하게)
    # 상위 5개 연관어만 저장
    final_related = {}
    for k, v in database["related_keywords"].items():
        final_related[k] = [pair[0] for pair in v.most_common(5)]
    database["related_keywords"] = final_related
    
    print(f"=====================================================================")
    print(f"   GENERATION COMPLETE")
    print(f"   - Total Documents: {doc_id:,}")
    print(f"   - Total Entries: {entry_count:,}")
    print(f"   - Categories: {list(topics.keys())}")
    print(f"=====================================================================")

    # 저장
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    output_path = os.path.join(data_dir, 'manual_db.json')
    os.makedirs(data_dir, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    print(f"Dataset securely saved to {output_path}")
    print(f"Time Elapsed: {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    generate_manual_db()
