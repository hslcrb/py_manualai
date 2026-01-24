import math

def get_ngrams(text, n=2):
    """
    Generate character-level N-grams from text.
    '안녕하세요' (n=2) -> ['안녕', '녕하', '하세', '세요']
    This helps in partial matching and overcoming typos.
    """
    text = text.replace(" ", "")  # Ignore spaces for N-gram
    if len(text) < n:
        return [text]
    return [text[i:i+n] for i in range(len(text)-n+1)]

def levenshtein_distance(s1, s2):
    """
    Calculates the Levenshtein distance between two strings using dynamic programming.
    Pure Python implementation.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def calculate_similarity_score(query, target):
    """
    Hybrid scoring: Keyword Overlap (Weighted) + N-gram Jaccard
    Optimized for Korean by ignoring common particles (Josa).
    """
    if not query or not target: return 0.0
    
    # 0. Preprocessing (Stopwords removal)
    # 조사를 제거하여 핵심 의미만 남김
    stopwords = {"은", "는", "이", "가", "을", "를", "의", "에", "에서", "한테", "로", "으로", "하다", "한", "합니다", "요", "죠"}
    
    def get_keywords(text):
        words = text.split()
        return {w for w in words if w not in stopwords and len(w) > 1} # 1글자 제외 (노이즈 방지)

    q_keywords = get_keywords(query)
    t_keywords = get_keywords(target)
    
    if not q_keywords: # 키워드가 다 제거되면 원본 사용
        q_keywords = set(query.split())
        
    # 1. Keyword Overlap Score (검색 엔진 핵심: 핵심 단어가 얼마나 겹치는가)
    # 타겟(DB문장)이 쿼리의 키워드를 얼마나 포함하고 있는가?
    overlap_count = 0
    for qk in q_keywords:
        # 완전 일치 또는 포함 관계 (e.g. "파이썬" in "파이썬은")
        match_found = False
        for tk in t_keywords:
            if qk in tk or tk in qk:
                match_found = True
                break
        
        # 키워드가 타겟 문장 전체 문자열 내에 포함되어 있어도 인정
        if not match_found and qk in target:
            match_found = True
            
        if match_found:
            overlap_count += 1
            
    keyword_score = 0.0
    if len(q_keywords) > 0:
        keyword_score = overlap_count / len(q_keywords)
    
    # 2. Sequential N-gram Score (순서와 오타 보정)
    q_ngrams = set(get_ngrams(query, 2))
    t_ngrams = set(get_ngrams(target, 2))
    
    ngram_score = 0
    if q_ngrams and t_ngrams:
        intersection = len(q_ngrams.intersection(t_ngrams))
        union = len(q_ngrams.union(t_ngrams))
        ngram_score = intersection / union
        
    # 최종 점수: Max Strategy
    # 키워드가 정확히 매칭되면 그 점수를 쓰고 (의미 기반),
    # 오타가 많아서 키워드 매칭이 안 되더라도 형태적 유사성(N-gram)이 높으면 그 점수를 씀.
    final_score = max(keyword_score, ngram_score)
    
    return final_score
