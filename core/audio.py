import time
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

# Initialize local Faster-Whisper model ('base' for fast local inference)
print("Loading Faster-Whisper model...")
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")


def record_until_pause(
    samplerate: int = 16000,
    chunk_duration: float = 0.2,
    pause_threshold: float = 4.0,
    silence_rms_threshold: float = 0.015,
    max_duration: float = 60.0,
) -> str:
    """Records until the operator pauses speaking for `pause_threshold` seconds."""
    blocksize = int(samplerate * chunk_duration)
    chunks: list[np.ndarray] = []

    speech_started = False
    silence_elapsed = 0.0
    start_time = time.monotonic()
    last_tick = start_time

    print(
        f"\n[A.R.I.S.A. Audio Link]: Listening... "
        f"(speak freely; {pause_threshold:.0f}s pause ends turn)"
    )

    with sd.InputStream(
        samplerate=samplerate,
        channels=1,
        dtype="float32",
        blocksize=blocksize,
    ) as stream:
        while True:
            audio_chunk, _ = stream.read(blocksize)
            now = time.monotonic()
            dt = now - last_tick
            last_tick = now

            samples = audio_chunk.flatten()
            rms = float(np.sqrt(np.mean(np.square(samples)))) if samples.size else 0.0
            is_speaking = rms > silence_rms_threshold

            if is_speaking:
                speech_started = True
                silence_elapsed = 0.0
                chunks.append(samples)
            elif speech_started:
                chunks.append(samples)
                silence_elapsed += dt
                if silence_elapsed >= pause_threshold:
                    break

            if (now - start_time) >= max_duration:
                print("\n[A.R.I.S.A. Audio Link]: Max capture window reached.")
                break

    if not chunks:
        return ""

    audio_signal = np.concatenate(chunks)
    print("[A.R.I.S.A. Audio Link]: Transcribing audio stream...")
    segments, _ = whisper_model.transcribe(audio_signal, beam_size=5)

    transcript = "".join([segment.text for segment in segments]).strip()
    print(f"[Operator Spoken]: {transcript}")
    return transcript


def record_and_transcribe(duration: int = 5, samplerate: int = 16000) -> str:
    """Legacy fixed-duration helper kept for backwards compatibility."""
    print(f"\n[A.R.I.S.A. Audio Link]: Listening for {duration} seconds...")
    audio_data = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype=np.float32,
    )
    sd.wait()

    audio_signal = audio_data.flatten()
    print("[A.R.I.S.A. Audio Link]: Transcribing audio stream...")
    segments, _ = whisper_model.transcribe(audio_signal, beam_size=5)

    transcript = "".join([segment.text for segment in segments]).strip()
    print(f"[Operator Spoken]: {transcript}")
    return transcript


if __name__ == "__main__":
    text = record_until_pause(pause_threshold=4.0)
    print(f"Captured Text Result: {text}")