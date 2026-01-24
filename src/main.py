import sys
import time
from engine import ManualEngine

def type_effect(text, delay=0.015, color=None):
    if color: sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    if color: sys.stdout.write("\033[0m")
    print()

def print_banner():
    banner = r"""
========================================================================
   __  __                         _    _    ___   _   _  _ 
  |  \/  | __ _ _ __  _   _  __ _| |  / \  |_ _| / \ | || |
  | |\/| |/ _` | '_ \| | | |/ _` | | / _ \  | | / _ \| || |
  | |  | | (_| | | | | |_| | (_| | |/ ___ \ | |/ ___ \ || |
  |_|  |_|\__,_|_| |_|\__,_|\__,_|_/_/   \_\_/_/   \_\_||_| v7.0
 
        [ KNOWLEDGE DEMOCRATIZATION PROJECT : OBEDOR ]
        [ 1 MILLION+ ENCYCLOPEDIC DATA | HIGH-SPEED INFERENCE ]
========================================================================
"""
    print("\033[96m" + banner + "\033[0m")

def main():
    print_banner()
    print("System initializing Data Grids...")
    engine = ManualEngine()
    
    type_effect("\n[SYSTEM] Obedor AI is now synchronous with the global knowledge base.", delay=0.005, color="\033[90m")
    type_effect("[SYSTEM] Ready. Type your query to initiate deep search.", delay=0.005, color="\033[90m")
    print("\033[90m" + "-"*72 + "\033[0m")
    
    while True:
        try:
            print(f"\n\033[92mUSER >> \033[0m", end="")
            user_input = input().strip()
            
            if not user_input: continue
            if user_input.lower() in ['exit', 'quit', '종료']:
                type_effect("Gracefully shutting down Obedor system...")
                break
                
            result = engine.search(user_input)
            
            # 1. AI Featured Snippet (Gemini Style)
            print(f"\033[90m[INTEL] {result['strategy']} | {result['time']:.4f}s | Confidence: {result['confidence']:.2f}\033[0m")
            print("\n \033[1m● Obedor AI Answer\033[0m")
            print(" └─ ", end="")
            type_effect(result['ai_response'], delay=0.01, color="\033[93m")
            
            # 2. Search Results
            if result['search_results']:
                print(f"\n \033[1m● Related Knowledge Sources\033[0m")
                for i, res in enumerate(result['search_results']):
                    source = f"[{res['type']}/{res['category']}]"
                    print(f"   [{i+1}] \033[94m{res['title']}\033[0m \033[90m{source}\033[0m")
                    print(f"       \033[37m{res['content'][:150]}...\033[0m")
            
            # 3. Related Keywords
            if result['related']:
                print(f"\n \033[1m● People also search for\033[0m")
                print("   " + ", ".join([f"\033[96m#{kw}\033[0m" for kw in result['related']]))
                
            print("\n" + "\033[90m" + "."*72 + "\033[0m")
                
        except (KeyboardInterrupt, EOFError):
            print("\nForce termination received.")
            break

if __name__ == "__main__":
    main()
