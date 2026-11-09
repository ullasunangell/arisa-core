import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

# Initialize local Faster-Whisper model ('base' for fast local inference)
print("Loading Faster-Whisper model...")
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")

def record_and_transcribe(duration: int = 5, samplerate: int = 16000) -> str:
    """Records audio from the microphone for a set duration and transcribes it locally."""
    print(f"\n[A.R.I.S.A. Audio Link]: Listening for {duration} seconds...")
    
    # Record audio from default microphone
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.float32)
    sd.wait()
    
    audio_signal = audio_data.flatten()
    
    print("[A.R.I.S.A. Audio Link]: Transcribing audio stream...")
    segments, _ = whisper_model.transcribe(audio_signal, beam_size=5)
    
    transcript = " ".join([segment.text for segment in segments]).strip()
    print(f"[Operator Spoken]: {transcript}")
    
    return transcript

if __name__ == "__main__":
    text = record_and_transcribe(duration=5)
    print(f"Captured Text Result: {text}")