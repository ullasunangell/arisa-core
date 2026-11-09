import subprocess
import os
from ollama import chat

ARISA_SYSTEM_PROMPT = (
    "You are A.R.I.S.A. (Autonomous Real-time Intelligence & System Agent), "
    "an advanced local-first AI system engineered by Angell Data Intelligence. "
    "Your tone is formal, minimalist, crisp, and unbothered. "
    "You address the user strictly as 'Ma'am'. Keep responses concise and direct."
)

def speak(text):
    """Uses macOS native text-to-speech to voice A.R.I.S.A.'s responses."""
    clean_text = text.replace('"', '').replace('*', '')
    subprocess.run(["say", clean_text])

def query_arisa(prompt: str, voice_output: bool = True):
    print("Querying A.R.I.S.A. local engine...")
    response = chat(
        model='llama3:8b',
        messages=[
            {'role': 'system', 'content': ARISA_SYSTEM_PROMPT},
            {'role': 'user', 'content': prompt},
        ]
    )
    answer = response['message']['content']
    
    if voice_output:
        speak(answer)
        
    return answer

if __name__ == "__main__":
    print("Initializing A.R.I.S.A. Core Engine...")
    test_prompt = "Status check, Arisa. Are systems operational?"
    print(f"\nUser: {test_prompt}")
    reply = query_arisa(test_prompt)
    print(f"\nA.R.I.S.A.: {reply}")