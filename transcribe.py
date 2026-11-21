from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe("input.mp4")

with open("transcript.txt", "w", encoding="utf-8") as f:
    for s in segments:
        line = f"[{s.start:.1f} to {s.end:.1f}] {s.text.strip()}"
        print(line)
        f.write(line + "\n")

print("Done: transcript.txt created")