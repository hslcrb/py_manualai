import sys
import time
from engine import ManualEngine

def type_effect(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_banner():
    banner = r"""
===========================================================
  __  __                         _    _    ___ 
 |  \/  | __ _ _ __  _   _  __ _| |  / \  |_ _|
 | |\/| |/ _` | '_ \| | | |/ _` | | / _ \  | | 
 | |  | | (_| | | | | |_| | (_| | |/ ___ \ | | 
 |_|  |_|\__,_|_| |_|\__,_|\__,_|_/_/   \_\___|
 
        [ HIGH-SPEED MANUAL INTELLIGENCE ]
        [ NO NEURAL NETWORKS DETECTED ]
===========================================================
"""
    print(banner)

def main():
    print_banner()
    print("System initializing...")
    engine = ManualEngine()
    
    type_effect("\n[SYSTEM] ManualAI is online via Command Line Interface.")
    type_effect("[SYSTEM] Ready to process extensive pre-calculated datasets.")
    print("-----------------------------------------------------------")
    
    while True:
        try:
            user_input = input("\nUSER >> ")
            if user_input.lower() in ['exit', 'quit', '종료']:
                type_effect("ManualAI shutting down...")
                break
                
            if result := engine.search(user_input):
                 # 검색 결과 메타데이터 표시 (사용자가 "고도의 검색"임을 느끼게 하기 위함)
                print(f"\n[LOGIC] Strategy: {result['strategy']} | Time: {result['time']:.6f}s | Confidence: {result['confidence']:.2f}")
                
                type_effect(f"AI >> {result['response']}")
                
        except KeyboardInterrupt:
            print("\nForce shutdown initiated.")
            sys.exit(0)

if __name__ == "__main__":
    main()
