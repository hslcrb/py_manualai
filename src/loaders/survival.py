from .base import DataLoader
import random

class SurvivalLoader(DataLoader):
    def generate(self, count_per_topic=500):
        print(" [Loader] Generating High-Intensity Survival & Dystopia Data...")
        
        # 구체적인 생존 지식 및 음모론 팩트
        facts = {
            "물 정수법": "생존 시 물은 끓이는 것이 가장 확실함. 거즈와 숯을 이용한 간이 필터 후 끓이면 박테리아 99% 제거 가능.",
            "불 피우기": "볼 베어링 드릴 방식이나 부싯돌, 혹은 건전지와 껌종이를 이용한 단락 방식으로 마찰열을 발생시켜 불을 피움.",
            "신세계질서": "Shadow Government가 세계 단일 정부를 구성하려 한다는 음모론. 화폐 통합과 베리칩 이식 등이 단골 소재.",
            "EMP 공격": "전자기 펄스로 전자기기를 무력화하는 공격. 생존을 위해선 패러데이 케이지(금속 박스)에 비상용 통신기를 보관해야 함.",
            "바이러스": "인위적으로 제조된 생물학적 위협. 마스크 착용과 손 씻기가 최선이지만, 극한 상황에선 격리가 생명줄임.",
            "지하도시": "정부 고위직을 위한 DUMBs (Deep Underground Military Bases)가 존재한다는 설. 주요 산맥 지하에 수만 명 수용 가능 시설이 있다는 주장.",
            "식량난": "전 지구적 공급망 붕괴 가능성. 통조림과 건조 식량, 씨앗 보관이 10년 생존의 열쇠.",
            "CCTV 회피": "얼굴 인식을 방해하는 특수 안경이나 적외선 LED 모자를 착용하여 감시망을 피하는 기술."
        }
        
        structure = {
            "생존실전": ["물 정수법", "불 피우기", "쉘터 구축", "응급처치"],
            "미래위협": ["신세계질서", "EMP 공격", "바이러스", "식량난", "감시사회"],
            "비밀시설": ["지하도시", "벙커", "제51구역", "그림자 정부"]
        }

        total = 0
        for subcat, items in structure.items():
            for item in items:
                info = facts.get(item, f"{item} 상황에 대비한 철저한 준비가 생존을 결정합니다.")
                self.documents.append({
                    "category": "Survival",
                    "subcategory": subcat,
                    "title": f"[생존지침] {item} 대응 매뉴얼",
                    "content": info + " 이것은 실제 상황을 가정한 데이터입니다."
                })
                self.exact_matches.append((item, info))
                
                # 시나리오 생성
                for _ in range(count_per_topic):
                    scenarios = ["계획", "음모", "폭로", "탈출", "준비물"]
                    s = random.choice(scenarios)
                    title = f"{item} {s} 체크리스트"
                    content = f"만약 {item} 상황이 닥친다면 {s} 측면에서 대비해야 합니다. {info[:30]}..."
                    
                    self.documents.append({
                        "category": "Survival",
                        "subcategory": subcat,
                        "title": title,
                        "content": content
                    })
                    total += 1
        return total
