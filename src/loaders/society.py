from .base import DataLoader
import random

class SocietyLoader(DataLoader):
    def generate(self, count_per_topic=500):
        print(" [Loader] Generating Society (Politics, Economy) Data...")
        
        structure = {
            "정치": ["선거", "민주주의", "국회", "대통령", "정책", "외교", "UN", "법률"],
            "사회이슈": ["저출산", "고령화", "환경오염", "젠더갈등", "MZ세대", "부동산"],
            "경제": ["금리", "환율", "삼성전자", "테슬라", "재테크", "연금"],
            "역사": ["세계대전", "조선왕조", "산업혁명", "냉전", "로마제국"]
        }
        
        titles = [
            "{item}의 역사와 현재", "{item} 문제의 해결책은?",
            "2026년 {item} 전망 보고서", "{cat} 분야 핫 키워드: {item}",
            "{item}에 대한 찬반 논란 정리", "교과서에 없는 {item} 이야기"
        ]
        
        contents = [
            "{item}은 현대 {cat}의 가장 중요한 주제입니다. {comp}와 밀접하게 연관되어 있습니다.",
            "최근 통계에 따르면 {item} 지수가 급변하고 있습니다. 전문가들은 {comp} 현상과 비슷하다고 분석합니다.",
            "{item} 문제를 해결하기 위해서는 시민들의 관심이 필요합니다.",
            "{item}의 기원은 {comp} 시대까지 거슬러 올라갑니다."
        ]

        total = 0
        for subcat, items in structure.items():
            for item in items:
                others = [x for x in items if x != item] or ["역사"]
                
                for _ in range(count_per_topic):
                    comp = random.choice(others)
                    title = random.choice(titles).format(item=item, cat=subcat)
                    content = random.choice(contents).format(item=item, comp=comp, cat=subcat)
                    
                    self.documents.append({
                        "category": "Society",
                        "subcategory": subcat,
                        "title": title,
                        "content": content
                    })
                    self.related_keywords.append((item, comp, 1))
                    total += 1
        return total
