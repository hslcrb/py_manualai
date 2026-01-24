from .base import DataLoader
import random

class TechLoader(DataLoader):
    def generate(self, count_per_topic=500):
        print(" [Loader] Generating High-Quality Technology Encyclopedia...")
        
        # 실제 지식 데이터 기반 사실군 (Fact Base)
        facts = {
            "파이썬": "1991년 귀도 반 로섬이 개발한 언어. 가독성이 높고 풍부한 라이브러리로 데이터 과학과 AI의 표준이 됨.",
            "리눅스": "리누스 토발즈가 개발한 유닉스 계열 오픈소스 OS. 전 세계 서버의 90% 이상과 안드로이드 OS의 기반.",
            "알고리즘": "문제를 해결하기 위한 단계적 절차. 컴퓨터 과학에서는 효율적인 정렬, 검색, 데이터 처리를 위한 수식.",
            "인공지능": "인간의 지능적 능력을 모방하는 기술. 머신러닝과 딥러닝을 통해 데이터로부터 학습하고 예측을 수행함.",
            "양자컴퓨터": "큐비트를 사용하여 중첩과 얽힘 현상을 이용하는 컴퓨터. 기존 슈퍼컴퓨터로 수만 년 걸리는 계산을 수 분 만에 해결 가능.",
            "반도체": "도체와 부도체의 중간 성질을 가진 물질. 삼성전자와 SK하이닉스가 선도하는 메모리 반도체와 시스템 반도체로 구분됨.",
            "도커": "컨테이너 기반 가상화 플랫폼. 애플리케이션을 환경에 구애받지 않고 실행할 수 있게 해주는 혁신적 도구.",
            "쿠버네티스": "컨테이너화된 애플리케이션의 배포, 확장, 관리를 자동화하는 오케스트레이션 시스템. 구글에서 개발.",
            "6G 네트워크": "5G보다 50배 빠른 테라헤르츠 대역 통신. 홀로그램 통신과 초정밀 실시간 원격 수술을 지향함.",
            "AGI": "범용 인공지능. 특정 업무를 넘어 인간과 대등하거나 뛰어난 지능을 전 영역에서 발휘하는 인공지능의 최종 단계."
        }
        
        structure = {
            "소프트웨어": ["파이썬", "알고리즘", "인공지능", "리눅스", "도커", "쿠버네티스"],
            "하드웨어": ["반도체", "양자컴퓨터", "CPU", "GPU"],
            "미래전망": ["AGI", "6G 네트워크", "특이점", "뉴럴링크"]
        }

        total = 0
        for subcat, items in structure.items():
            for item in items:
                # 1. 고품질 사실 기반 문서 (하나씩 생성)
                base_info = facts.get(item, f"{item}은(는) IT {subcat} 분야의 핵심 기술 중 하나입니다.")
                self.documents.append({
                    "category": "Technology",
                    "subcategory": subcat,
                    "title": f"[백과사전] {item}이란 무엇인가?",
                    "content": base_info + " 더 자세한 정보는 관련 문서를 참고하십시오."
                })
                self.exact_matches.append((item, base_info))
                
                # 2. 대량의 관련 뉴스/블로그 데이터 생성 (템플릿 다양화)
                verbs = ["주목하라", "시장을 뒤흔들다", "혁신적이다", "미래를 바꾸다", "논란이 되다", "필수다"]
                for _ in range(count_per_topic):
                    v = random.choice(verbs)
                    title = f"{item}, 왜 {v}?"
                    content = f"최근 {subcat} 분야의 분석에 따르면 {item}은(는) {v}. 특히 {base_info[:20]} 관련 기술이 부각되고 있습니다."
                    
                    self.documents.append({
                        "category": "Technology",
                        "subcategory": subcat,
                        "title": title,
                        "content": content
                    })
                    total += 1
        return total
