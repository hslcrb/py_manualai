from .base import DataLoader
import random

class SurvivalLoader(DataLoader):
    def generate(self, count_per_topic=500):
        print(" [Loader] Generating Survival & Dystopia Data...")
        
        structure = {
            "생존기술": ["물 정수법", "불 피우기", "쉘터 구축", "응급처치", "매듭법", "통조림 보관"],
            "디스토피아": ["감시사회", "신세계질서", "EMP 공격", "식량난", "바이러스", "벙커"],
            "도시생존": ["CCTV 회피", "파쿠르", "도심 채집", "은신처 찾기", "폭동 대처"],
            "음모론": ["그림자 정부", "외계인", "달 착륙", "지하도시", "제51구역"]
        }
        
        titles = [
            "{item} 상황 발생 시 행동요령", "{item}의 진실을 파헤치다",
            "당신이 몰랐던 {item}의 비밀", "생존을 위한 {item} 마스터하기",
            "{item}: 인류 최후의 날 시나리오",
            "정부가 숨기고 있는 {item}", "{item} 대비 필수 장비 리스트"
        ]
        
        contents = [
            "{cat} 상황에서 가장 중요한 것은 {item}입니다. 침착하게 대응하세요.",
            "누군가 {item}을 조종하고 있습니다. 신세계질서가 도래하기 전 대비해야 합니다.",
            "{item}에 대한 정보는 통제되고 있습니다. 이 문서는 귀중한 생존 지침서입니다.",
            "만약 {item} 사태가 발생한다면, 즉시 {comp}를 확보하십시오."
        ]

        # Generate
        total = 0
        for subcat, items in structure.items():
            for item in items:
                others = [x for x in items if x != item] or ["비상식량"]
                
                for _ in range(count_per_topic):
                    comp = random.choice(others)
                    
                    title = random.choice(titles).format(item=item)
                    content = random.choice(contents).format(item=item, comp=comp, cat=subcat)
                    
                    self.documents.append({
                        "category": "Survival",
                        "subcategory": subcat,
                        "title": title,
                        "content": content
                    })
                    self.related_keywords.append((item, comp, 1))
                    total += 1
                    
        return total
