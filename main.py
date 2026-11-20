import time
from core.audio import record_until_pause
from core.engine import ArisaEngine, query_arisa


def run_arisa_loop():
    engine = ArisaEngine()

    greeting = "Arisa online. Systems initialized. Listening, ma'am."
    print(f"\n[A.R.I.S.A.]: {greeting}")
    engine.speak(greeting)

    exit_triggers = [
        "exit",
        "quit",
        "bye",
        "goodbye",
        "stop",
        "cancel",
        "shut down",
        "stop listening",
    ]

    while True:
        try:
            user_input = record_until_pause(pause_threshold=4.0)

            if not user_input.strip():
                continue

            cleaned_input = user_input.lower().strip()
            print(f"\n[Operator]: {user_input}")

            if any(trigger in cleaned_input for trigger in exit_triggers):
                farewell = "Signing off. Goodbye, ma'am."
                print(f"\n[A.R.I.S.A.]: {farewell}")
                engine.speak(farewell)
                break

            response_text = query_arisa(user_input)
            print(f"[A.R.I.S.A.]: {response_text}")

            engine.speak(response_text)
            time.sleep(1)

        except KeyboardInterrupt:
            print("\n[A.R.I.S.A.]: Manual override detected. Offline.")
            break
        except Exception as e:
            print(f"\n[System Error]: {e}")
            break


if __name__ == "__main__":
    run_arisa_loop()