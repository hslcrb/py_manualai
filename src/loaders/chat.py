from .base import DataLoader

class ChatLoader(DataLoader):
    """
    Standard Chat Logic and Greetings.
    """
    def generate(self, count_per_topic=1):
        print(" [Loader] Injecting Core Chat Intelligence...")
        
        greetings = [
            ("안녕", "안녕하세요! 지식의 민주화를 꿈꾸는 ManualAI(Obedor) v7.0입니다. 무엇을 도와드릴까요?"),
            ("안녕하세요", "반갑습니다. GPU 없이도 100만 건 이상의 지식을 순식간에 찾는 고성능 Obedor 엔진입니다."),
            ("하이", "시스템 최적화 상태입니다. 오늘 탐험하고 싶은 지식 분야가 있나요? (IT, 생존, 사회, 생활 등)"),
            ("hello", "Hello! I am ManualAI. How can I assist you with my massive knowledge base today?"),
            ("누구야", "저는 ManualAI, 코드네임 Obedor입니다. 딥러닝 없이 오직 알고리즘과 거대 DB로만 동작하는 고성능 AI 에이전트입니다."),
            ("정체", "저는 데이터베이스 기반의 초고속 전문 검색 엔진이자, 지식의 민주화를 실현하는 매뉴얼 지능 체계입니다."),
            ("도와줘", "찾고 싶은 키워드를 입력하세요. 예: '리눅스', '신세계질서', '김치찌개 레시피', '비트코인 전망'"),
            ("기능", "저는 대규모 데이터 검색, 연관 검색어 추천, 지식 요약(Featured Snippet) 기능을 제공합니다."),
            ("버전", "현재 ManualAI v7.0 (Massive Scale Edition) 버전이 가동 중입니다."),
            ("민주화", "지식의 민주화란 고가의 GPU나 서버 없이도 누구나 자신의 로컬 환경에서 거대한 지식 창고를 소유하고 검색할 수 있음을 의미합니다.")
        ]
        
        # Variations for robustness
        expanded = []
        for q, r in greetings:
            expanded.append((q, r))
            expanded.append((q + "?", r))
            expanded.append((q + "!", r))
            expanded.append((q + " ", r))
            
        for q, r in expanded:
            self.exact_matches.append((q, r))
            
        return len(self.exact_matches)
