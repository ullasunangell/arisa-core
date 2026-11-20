import subprocess
import ollama

DEFAULT_CHAT_MODEL = "llama3:8b"
DEFAULT_CODER_MODEL = "qwen2.5-coder:7b"

CODE_KEYWORDS = [
    "code",
    "python",
    "script",
    "function",
    "class",
    "bug",
    "error",
    "traceback",
    "refactor",
    "sql",
    "dbt",
    "git",
    "docker",
    "api",
    "regex",
    "json",
    "bash",
    "terminal",
]


def select_model(prompt: str) -> str:
    """Routes coding/technical prompts to Qwen 2.5 Coder and general prompts to Llama 3."""
    lowered = prompt.lower()
    if any(keyword in lowered for keyword in CODE_KEYWORDS):
        return DEFAULT_CODER_MODEL
    return DEFAULT_CHAT_MODEL


class ArisaEngine:
    def __init__(
        self,
        model: str = DEFAULT_CHAT_MODEL,
        coder_model: str = DEFAULT_CODER_MODEL,
        voice: str = "Serena",
    ):
        self.model = model
        self.coder_model = coder_model
        self.voice = voice

    def speak(self, text: str):
        """Uses macOS native 'say' command for British RP TTS."""
        try:
            subprocess.run(["say", "-v", self.voice, text], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[TTS Error]: {e}")

    def query(self, prompt: str, model: str | None = None) -> str:
        """Queries the local Ollama instance using an explicit model or automatic routing."""
        target_model = model or select_model(prompt)
        try:
            response = ollama.chat(
                model=target_model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Arisa, an advanced local-first autonomous AI system assistant "
                            "created for software engineering and personal data management. "
                            "Be concise, precise, professional, and address the user respectfully as 'ma'am'."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            return response["message"]["content"]
        except Exception as e:
            return f"Error communicating with local LLM engine ({target_model}): {e}"


def query_arisa(prompt: str, model: str | None = None) -> str:
    """Convenience wrapper function for querying."""
    engine = ArisaEngine()
    return engine.query(prompt, model=model)