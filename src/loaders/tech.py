from .base import DataLoader
import random

class TechLoader(DataLoader):
    def generate(self, count_per_topic=500):
        print(" [Loader] Generating Technology Data...")
        
        structure = {
            "소프트웨어": ["파이썬", "C++", "자바", "리눅스", "도커", "쿠버네티스", "알고리즘", "인공지능"],
            "하드웨어": ["CPU", "GPU", "RAM", "SSD", "메인보드", "양자컴퓨터", "반도체"],
            "보안": ["해킹", "방화벽", "랜섬웨어", "제로트러스트", "화이트해커", "암호학"],
            "미래기술": ["AGI", "특이점", "뉴럴링크", "메타버스", "블록체인", "6G 네트워크"]
        }
        
        titles = [
            "{item} 완벽 가이드", "{item}의 미래 전망", "초보자를 위한 {item} 설명",
            "{item} vs {comp} 비교 분석", "{item} 최신 동향 리포트",
            "개발자가 말하는 {item}의 진실", "2026년 {item} 트렌드"
        ]
        
        contents = [
            "{item}은(는) 현대 기술의 핵심입니다. 특히 {cat} 분야에서 중요합니다.",
            "{item} 기술이 급격히 발전하고 있습니다. 전문가들은 {item}이 {comp}를 대체할 것이라 봅니다.",
            "실무에서 {item}을(를) 활용하는 팁을 공개합니다. {cat} 시장의 변화를 주목하세요.",
            "속보: {item} 관련 신기술이 발표되었습니다."
        ]

        # Generate
        total = 0
        for subcat, items in structure.items():
            for item in items:
                # Comparison Item
                others = [x for x in items if x != item]
                
                # Bulk Generation
                for _ in range(count_per_topic):
                    comp = random.choice(others) if others else "기존 기술"
                    
                    t_tmpl = random.choice(titles)
                    c_tmpl = random.choice(contents)
                    
                    title = t_tmpl.format(item=item, comp=comp)
                    content = c_tmpl.format(item=item, comp=comp, cat=subcat)
                    
                    self.documents.append({
                        "category": "Technology",
                        "subcategory": subcat,
                        "title": title,
                        "content": content
                    })
                    
                    self.related_keywords.append((item, comp, 1))
                    if _ % 20 == 0:
                        self.exact_matches.append((title, content))
                        
                    total += 1
        return total
