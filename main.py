import sys
from core.audio import record_and_transcribe
from core.engine import query_arisa

def run_arisa_loop():
    print("==================================================")
    print(" A.R.I.S.A. Core System :: Voice Interface Online ")
    print("==================================================")
    
    while True:
        try:
            # 1. Listen to operator microphone input
            user_speech = record_and_transcribe(duration=5)
            
            if not user_speech:
                print("[System]: No audio detected. Retrying...")
                continue
                
            # Exit condition
            if "exit" in user_speech.lower() or "terminate" in user_speech.lower():
                print("[A.R.I.S.A.]: Standing down, Ma'am.")
                break
            
            # 2. Query the local Llama 3 engine
            response = query_arisa(user_speech)
            print(f"\n[A.R.I.S.A.]: {response}\n")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n[System]: Interrupted by operator. Shutting down...")
            sys.exit(0)

if __name__ == "__main__":
    run_arisa_loop()