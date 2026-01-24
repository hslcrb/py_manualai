def highlight_text(text, queries, color_code="\033[93m"): # Default Yellow
    """
    Highlights query terms in the text using ANSI color codes.
    Case-insensitive matching.
    """
    reset_code = "\033[0m"
    lower_text = text.lower()
    
    # 인덱스 위치를 찾아서 마킹 (원본 텍스트 보존을 위함)
    # 간단하게 replace 사용시 대소문자 문제 발생하므로 정규식이나 토큰 교체가 나음.
    # 여기서는 성능 떄문에 단순 replacer 루프를 돌림 (키워드가 적으므로)
    
    highlighted = text
    for q in queries:
        if not q or len(q) < 1: continue
        # Find all occurrences
        start = 0
        while True:
            idx = highlighted.lower().find(q.lower(), start)
            if idx == -1: break
            
            # ANSI 코드가 이미 삽입된 부분 건너뛰기 방지 로직 필요하나
            # 간단하게 하기 위해 매번 replace하는 방식, 하지만 이미 color code 들어간거 재매칭 안되게 조심
            # 단순 replace로 개선: 원본 문자열의 해당 부분을 감싸서 교체
            
            # 가장 확실한 방법: re.sub with ignore case
            import re
            pattern = re.compile(re.escape(q), re.IGNORECASE)
            highlighted = pattern.sub(rf"{color_code}\g<0>{reset_code}", highlighted)
            break # 중복 컬러링 방지를 위해 키워드당 한 번의 패스만(re.sub은 전체 교체함)
            
    return highlighted

def get_ngrams(text, n=2):
    """
    Generate character-level N-grams from text.
    """
    text = text.replace(" ", "")
    if len(text) < n:
        return [text]
    return [text[i:i+n] for i in range(len(text)-n+1)]

def calculate_similarity_score(query, target):
    """
    Hybrid scoring: Keyword Overlap (Weighted) + N-gram Jaccard
    """
    if not query or not target: return 0.0
    
    stopwords = {"은", "는", "이", "가", "을", "를", "의", "에", "에서", "한테", "로", "으로", "하다", "한", "합니다", "요", "죠"}
    
    def get_keywords(text):
        words = text.split()
        return {w for w in words if w not in stopwords and len(w) > 1}

    q_keywords = get_keywords(query)
    t_keywords = get_keywords(target)
    
    if not q_keywords:
        q_keywords = set(query.split())
        
    overlap_count = 0
    for qk in q_keywords:
        match_found = False
        for tk in t_keywords:
            if qk in tk or tk in qk:
                match_found = True
                break
        
        if not match_found and qk in target:
            match_found = True
            
        if match_found:
            overlap_count += 1
            
    keyword_score = 0.0
    if len(q_keywords) > 0:
        keyword_score = overlap_count / len(q_keywords)
    
    q_ngrams = set(get_ngrams(query, 2))
    t_ngrams = set(get_ngrams(target, 2))
    
    ngram_score = 0
    if q_ngrams and t_ngrams:
        intersection = len(q_ngrams.intersection(t_ngrams))
        union = len(q_ngrams.union(t_ngrams))
        ngram_score = intersection / union
        
    return max(keyword_score, ngram_score)
