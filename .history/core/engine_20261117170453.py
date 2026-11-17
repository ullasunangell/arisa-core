import subprocess
import ollama

class ArisaEngine:
    def __init__(self, model: str = "llama3:8b", voice: str = "Serena"):
        self.model = model
        self.voice = voice  # macOS British RP voice (or default)

    def speak(self, text: str):
        """Uses macOS native 'say' command for British RP TTS."""
        try:
            # Clean text slightly for shell safety if needed
            subprocess.run(["say", "-v", self.voice, text], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[TTS Error]: {e}")

    def query(self, prompt: str) -> str:
        """Queries the local Ollama instance."""
        try:
            response = ollama.chat(model=self.model, messages=[
                {"role": "system", "content": "You are Arisa, an advanced local-first autonomous AI system assistant created for software engineering and personal data management. Be concise, precise, professional, and address the user respectfully as 'ma'am'."},
                {"role": "user", "content": prompt}
            ])
            return response['message']['content']
        except Exception as e:
            return f"Error communicating with local LLM engine: {e}"

def query_arisa(prompt: str) -> str:
    """Convenience wrapper function for querying."""
    engine = ArisaEngine()
    return engine.query(prompt)