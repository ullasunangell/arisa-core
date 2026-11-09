import sys
import ollama

ARISA_SYSTEM_PROMPT = (
    "You are A.R.I.S.A. (Autonomous Real-time Intelligence & System Agent), "
    "a professional, sharp, and highly secure AI intelligence engineered by Miss Angell. "
    "Your operator is addressed strictly as 'Ma'am'. Your tone is crisp, minimalist, unbothered, "
    "and intensely competent. Provide concise, high-signal technical responses without fluff."
)

def query_arisa(prompt: str, model: str = "llama3:8b") -> str:
    """Sends a prompt to the local Ollama instance wrapped in A.R.I.S.A.'s persona."""
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": ARISA_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        return response['message']['content']
    except Exception as e:
        return f"[System Error]: Failed to reach local Ollama backend -> {e}"

if __name__ == "__main__":
    print("Initializing A.R.I.S.A. Core Engine...")
    test_prompt = "Status check, Arisa. Are systems operational?"
    print(f"\nUser: {test_prompt}")
    
    reply = query_arisa(test_prompt)
    print(f"\nA.R.I.S.A.: {reply}")