import sys
import time
from core.audio import record_and_transcribe
from core.engine import query_arisa, ArisaEngine

def run_arisa_loop():
    engine = ArisaEngine()
    
    # Initial greeting via British RP TTS
    greeting = "A.R.I.S.A. online. Systems initialized. Listening, ma'am."
    print(f"\n[A.R.I.S.A.]: {greeting}")
    engine.speak(greeting)

    while True:
        try:
            # 1. Listen and transcribe from microphone (5-second window per trigger)
            user_input = record_and_transcribe(duration=5)
            
            if not user_input.strip():
                continue

            # Check for exit/shutdown triggers naturally
            if any(exit_word in user_input.lower() for exit_word in ["shut down", "exit arisa", "stop listening"]):
                farewell = "Shutting down systems. Goodbye, ma'am."
                print(f"\n[A.R.I.S.A.]: {farewell}")
                engine.speak(farewell)
                break

            print(f"\n[Operator]: {user_input}")

            # 2. Query local Ollama engine (using Llama 3)
            response_text = query_arisa(user_input)
            print(f"[A.R.I.S.A.]: {response_text}")

            # 3. Vocalize response via macOS native TTS (Serena RP)
            engine.speak(response_text)
            
            # Brief pause before next listening window
            time.sleep(1)

        except KeyboardInterrupt:
            print("\n[A.R.I.S.A.]: Manual override detected. Offline.")
            break
        except Exception as e:
            print(f"\n[System Error]: {e}")
            break

if __name__ == "__main__":
    run_arisa_loop()