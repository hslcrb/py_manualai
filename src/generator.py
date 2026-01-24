import json
import itertools
from collections import defaultdict
import time
import os
import random
from utils import get_ngrams

def generate_manual_db():
    print("Initializing MASSIVE ManualAI Database Generation Protocol (PORTAL SCALE)...")
    
    # --- 1. 대화형 데이터 (Existing) ---
    subjects = ["나", "너", "우리", "그", "그녀", "사람들", "세상", "우주", "AI", "파이썬", "코드", "사랑", "인생", "꿈"]
    verbs = ["좋아해", "싫어해", "알아", "몰라", "공부해", "생각해", "느껴", "만들어", "부셔", "도와줘", "알려줘"]
    adjectives = ["어렵다", "쉽다", "재밌다", "슬프다", "기쁘다", "화난다", "행복하다"]
    
    # --- 2. 정보성 데이터 (New: Portal Search Style) ---
    # 실제 검색엔진처럼 다양한 주제의 "지식 문서"를 생성
    knowledge_base = [
        {"category": "IT", "title": "파이썬 프로그래밍 가이드", "content": "파이썬은 1991년 귀도 반 로섬이 발표한 프로그래밍 언어입니다. 문법이 간결하고 가독성이 좋아 초보자에게 인기가 많습니다. 데이터 과학, 웹 개발 등 다양한 분야에서 사용됩니다."},
        {"category": "IT", "title": "리눅스 운영체제 기초", "content": "리눅스는 리누스 토발즈가 개발한 오픈 소스 운영체제 커널입니다. 서버 시장에서 압도적인 점유율을 자랑하며, 안정성과 보안성이 뛰어납니다."},
        {"category": "Cooking", "title": "김치찌개 맛있게 끓이는 법", "content": "잘 익은 김치를 참기름에 달달 볶다가 돼지고기를 넣고 육수를 부어 끓입니다. 다진 마늘, 대파, 두부를 넣고 푹 끓이면 완성입니다."},
        {"category": "Health", "title": "하루 물 권장 섭취량", "content": "세계보건기구(WHO)에 따르면 성인의 하루 물 권장 섭취량은 약 1.5리터에서 2리터입니다. 충분한 수분 섭취는 건강 유지에 필수적입니다."},
        {"category": "History", "title": "임진왜란의 역사", "content": "1592년 일본이 조선을 침략하여 일어난 전쟁입니다. 이순신 장군의 활약과 의병들의 저항으로 조선이 국난을 극복하였습니다."},
        {"category": "Science", "title": "상대성 이론 개요", "content": "알베르트 아인슈타인이 발표한 이론으로, 특수 상대성 이론과 일반 상대성 이론으로 나뉩니다. 시간과 공간이 절대적이지 않음을 증명했습니다."},
        {"category": "Travel", "title": "제주도 여행 코스 추천", "content": "제주도는 한국의 아름다운 섬입니다. 성산일출봉, 한라산, 우도 등 자연 경관이 뛰어나며 흑돼지, 갈치조림 등 먹거리가 풍부합니다."}
    ]

    database = {
        "meta": {
            "version": "3.0 (Portal Search Edition)",
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_entries": 0
        },
        "exact_match": {}, 
        "documents": [], # BM25 검색용 문서 리스트 (id, content, keywords)
        "keyword_index": defaultdict(list),
        "ngram_index": defaultdict(list)
    }

    entry_count = 0
    doc_id = 0

    # 1. 지식 문서 확장 (Knowledge Amplification)
    # 각 지식 문서를 기반으로 수많은 변형 질문/검색어 생성
    print("Generating Knowledge Base...")
    for kb in knowledge_base:
        # 원본 문서 등록
        database["documents"].append({
            "id": doc_id,
            "type": "knowledge",
            "title": kb["title"],
            "content": kb["content"],
            "keywords": kb["title"].split() + kb["content"].split()
        })
        
        # 검색어 매핑 (문서 타이틀 및 내용을 검색어로)
        queries = [
            kb["title"], 
            f"{kb['category']} 정보", 
            f"{kb['title']} 알려줘",
            f"{kb['title']}에 대해 설명해줘"
        ]
        
        # 내용에서 명사 추출하여 검색어 생성 (간이)
        words = kb["content"].split()
        for i in range(len(words)-1):
            queries.append(f"{words[i]} {words[i+1]}") # Bigram 검색어
        
        for q in queries:
            database["exact_match"][q] = [kb["content"]] # 검색 시 내용 반환
            
            # 인덱싱
            for word in q.split():
                database["keyword_index"][word].append(str(doc_id)) # 키워드 -> 문서 ID 매핑
            
            entry_count += 1
            
        doc_id += 1

    # 2. 대화형 데이터 생성 (기존 로직 유지 + 확장)
    print("Generating Dialogue Patterns...")
    templates = [
        {"q": "{subject} {verb}", "r": "{subject}가 {verb}한다니 흥미롭군요."},
        {"q": "{subject} {adjective}", "r": "{subject} 참 {adjective}하죠."},
        {"q": "{subject} {verb} {adjective}", "r": "정말 복합적인 상황이네요."}
    ]
    
    # 콤비네이션 로직 단순화하여 속도 향상시키되 규모 유지
    combined = list(itertools.product(subjects, verbs)) # suject + verb
    for s, v in combined:
        q = f"{s} {v}"
        r = [f"{s}에 대해 {v}라고 생각하시는군요."]
        
        # 문서로 등록 (BM25 검색 대상이 되도록)
        database["documents"].append({
            "id": doc_id,
            "type": "chat",
            "title": "Dialogue",
            "content": f"User said {q}. System responds: {r[0]}", 
            "keywords": q.split()
        })
        
        database["exact_match"][q] = r
        # 키워드 인덱싱
        for word in q.split():
            database["keyword_index"][word].append(str(doc_id))
        
        doc_id += 1
        entry_count += 1

    # 3. 노이즈 및 대규모 더미 데이터 (검색 볼륨감 확보)
    # 실제 포털처럼 느껴지게 하기 위해 '가상의 웹 문서'들을 대량 생성
    print("Simulating Web Documents...")
    web_keywords = ["뉴스", "블로그", "카페", "쇼핑", "동영상", "이미지"]
    topics = ["주식", "부동산", "게임", "스포츠", "연예", "정치", "경제"]
    
    for i in range(5000): # 5,000개의 가상 웹 문서 생성
        topic = random.choice(topics)
        category = random.choice(web_keywords)
        title = f"{topic} 관련 {category} 글 {i}"
        content = f"이것은 {topic}에 대한 {category} 테스트 데이터입니다. 번호 {i}."
        
        database["documents"].append({
            "id": doc_id,
            "type": "web",
            "title": title,
            "content": content,
            "keywords": title.split()
        })
        
        # 검색어 매핑
        database["exact_match"][title] = [content]
        for word in title.split():
            database["keyword_index"][word].append(str(doc_id))
        
        doc_id += 1
        entry_count += 1

    database["meta"]["total_entries"] = entry_count
    database["meta"]["total_documents"] = doc_id
    
    print(f"Generation Complete. Total Entries: {entry_count}, Total Documents: {doc_id}")
    
    # 저장
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    output_path = os.path.join(data_dir, 'manual_db.json')
    os.makedirs(data_dir, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    print(f"Database saved to {output_path}")

if __name__ == "__main__":
    generate_manual_db()
