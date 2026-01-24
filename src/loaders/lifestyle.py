from .base import DataLoader
import random

class LifeLoader(DataLoader):
    def generate(self, count_per_topic=500):
        print(" [Loader] Generating Practical Lifestyle & Cooking Data...")
        
        facts = {
            "김치찌개": "잘 익은 신김치를 참기름에 볶다가 돼지고기를 넣고 끓임. 설탕을 한 작은술 넣으면 김치의 신맛을 잡고 감칠맛이 살아남.",
            "라면 맛있게 끓이기": "물이 끓기 전에 스프를 먼저 넣고, 면을 괴롭히듯(공기와 접촉) 들었다 놨다 하면 면발이 쫄깃해짐. 식초 한 방울도 팁.",
            "로봇청소기": "Lidar 센서가 장착된 제품이 장애물 회피가 뛰어남. 최근엔 물걸레 세척 및 건조 기능까지 필수가 됨.",
            "식기세척기": "애벌세척 없이 바로 넣어도 되지만, 전용 세제를 사용해야 함. '삶의 질 3대장' 중 하나.",
            "미니멀라이프": "사용하지 않는 물건을 버리는 것이 아니라, 나에게 진짜 소중한 것만 남기는 삶의 방식.",
            "수비드": "진공 포장된 육류를 저온의 물에서 장시간 익히는 법. 육즙이 보존되어 스테이크 같은 고기가 매우 부드러워짐.",
            "홈카페": "에스프레소 머신과 핸드드립 도구로 집에서 고퀄리티 커피를 즐기는 법. 원두의 신선도가 맛의 80% 결정."
        }
        
        structure = {
            "요리레시피": ["김치찌개", "라면 맛있게 끓이기", "스테이크", "수비드", "된장찌개"],
            "가전/생활": ["로봇청소기", "식기세척기", "건조기", "미니멀라이프"],
            "취미/여가": ["홈카페", "캠핑", "독서", "식물 키우기"]
        }

        total = 0
        for subcat, items in structure.items():
            for item in items:
                info = facts.get(item, f"{item}에 대한 생활 팁입니다. 삶의 질을 높이세요.")
                self.documents.append({
                    "category": "Lifestyle",
                    "subcategory": subcat,
                    "title": f"[생활꿀팁] {item} 가이드",
                    "content": info
                })
                self.exact_matches.append((item, info))
                
                for _ in range(count_per_topic):
                    tips = ["초보용", "전문가용", "비교분석", "후기", "추천"]
                    t = random.choice(tips)
                    title = f"{item} {t}: 당신만 모르는 이야기"
                    content = f"많은 사람들이 {item}에 대해 잘못 알고 있습니다. {info[:20]} 관련 노하우를 소개합니다."
                    
                    self.documents.append({
                        "category": "Lifestyle",
                        "subcategory": subcat,
                        "title": title,
                        "content": content
                    })
                    total += 1
        return total
