from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    "input.mp4",
    task="transcribe",
    language="hi",
    initial_prompt="Aaj hum is topic ke baare mein baat karenge, bahut important hai.",
)

with open("transcript_hi.txt", "w", encoding="utf-8") as f:
    for s in segments:
        f.write(f"[{s.start:.1f} to {s.end:.1f}] {s.text.strip()}\n")

print("Done")