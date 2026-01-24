from .base import DataLoader
import random

class LifeLoader(DataLoader):
    def generate(self, count_per_topic=500):
        print(" [Loader] Generating Lifestyle (Cooking, Home) Data...")
        
        structure = {
            "요리": ["김치찌개", "파스타", "스테이크", "라면 맛있게 끓이기", "김밥", "된장찌개", "수비드"],
            "가전제품": ["로봇청소기", "식기세척기", "건조기", "에어드레서", "공기청정기", "AI 스피커"],
            "청소/정리": ["미니멀라이프", "옷장 정리", "화장실 청소", "곰팡이 제거", "분리수거"],
            "취미": ["캠핑", "낚시", "홈카페", "뜨개질", "식물 키우기", "독서"]
        }
        
        titles = [
            "{item} 추천 TOP 10", "{item} 내돈내산 솔직 후기",
            "집에서 {item} 완벽하게 즐기는 법", "{item} 실패하지 않는 꿀팁",
            "{item} vs {comp} 비교", "삶의 질을 높여주는 {item}"
        ]
        
        contents = [
            "오늘 저녁은 {item} 어떠신가요? {cat} 카테고리에서 가장 인기 많습니다.",
            "{item} 사용 후 삶이 달라졌습니다. 특히 {comp}보다 훨씬 편해요.",
            "{item} 할 때 가장 중요한 팁: {comp}를 활용하세요.",
            "전문가도 인정한 {item} 노하우를 공유합니다."
        ]

        total = 0
        for subcat, items in structure.items():
            for item in items:
                others = [x for x in items if x != item] or ["기본템"]
                
                for _ in range(count_per_topic):
                    comp = random.choice(others)
                    title = random.choice(titles).format(item=item, comp=comp)
                    content = random.choice(contents).format(item=item, comp=comp, cat=subcat)
                    
                    self.documents.append({
                        "category": "Lifestyle",
                        "subcategory": subcat,
                        "title": title,
                        "content": content
                    })
                    self.related_keywords.append((item, comp, 1))
                    total += 1
        return total
