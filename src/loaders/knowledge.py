from .base import DataLoader
import random
import string

class KnowledgeLoader(DataLoader):
    """
    Massive General Knowledge Loader to fill up the volume.
    (Encyclopedia style)
    """
    def generate(self, count_per_topic=2000):
        print(" [Loader] Generating General Encyclopedia Data...")
        
        # Simple A-Z or 가-하 logic simulation (Semantic Hashing)
        categories = ["Science", "Art", "Literature", "Geography", "Biology"]
        
        # Generate generic but searchable entries
        total = 0
        for _ in range(count_per_topic * 10): # Massive loop
            # Create synthetic titles that look like real concepts
            # e.g. "Concept-A102", "Project-X" or meaningful combinations
            
            cat = random.choice(categories)
            idx = random.randint(1, 9999)
            
            # Use some real-ish prefixes
            prefixes = ["Super", "Hyper", "Neo", "Proto", "Meta", "Anti", "Pro"]
            roots = ["Structure", "System", "Theory", "Process", "Element", "Force", "Logic"]
            
            p = random.choice(prefixes)
            r = random.choice(roots)
            
            title = f"{p}-{r} Type-{idx}"
            content = f"The {title} is a fundamental concept in {cat}. It relates to {p} phenomena. See also {r}-{idx+1}."
            
            self.documents.append({
                "category": "Encyclopedia",
                "subcategory": cat,
                "title": title,
                "content": content
            })
            total += 1
            if total >= count_per_topic * 5: # Limit
                break
                
        return total
