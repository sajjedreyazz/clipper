from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")


def run(task, filename):
    segments, info = model.transcribe("input.mp4", task=task)
    with open(filename, "w", encoding="utf-8") as f:
        for s in segments:
            f.write(f"[{s.start:.1f} to {s.end:.1f}] {s.text.strip()}\n")
    return info.language


lang = run("transcribe", "transcript_original.txt")
run("translate", "transcript_en.txt")
print("Detected language:", lang)
print("Done")