import sys
import time
from faster_whisper import WhisperModel

video = sys.argv[1] if len(sys.argv) > 1 else "input.mp4"
model_size = sys.argv[2] if len(sys.argv) > 2 else "auto"

try:
    import ctranslate2
    gpu = ctranslate2.get_cuda_device_count() > 0
except Exception:
    gpu = False


def load(use_gpu):
    size = model_size
    if size == "auto":
        size = "large-v3" if use_gpu else "base"
    device = "cuda" if use_gpu else "cpu"
    compute = "float16" if use_gpu else "int8"
    print(f"Device: {device}, model: {size}")
    return WhisperModel(size, device=device, compute_type=compute)


def start(model):
    segments, info = model.transcribe(video, task="transcribe", vad_filter=True)
    if info.language != "en":
        print(f"Language: {info.language}, translating to English")
        segments, info = model.transcribe(video, task="translate", vad_filter=True)
    return segments, info


try:
    segments, info = start(load(gpu))
except Exception as e:
    if not gpu:
        raise
    print("GPU failed, using CPU instead:", e)
    segments, info = start(load(False))

t0 = time.time()
with open("transcript_en.txt", "w", encoding="utf-8") as f:
    for s in segments:
        f.write(f"[{s.start:.1f} to {s.end:.1f}] {s.text.strip()}\n")
        f.flush()
        pct = 100 * s.end / max(info.duration, 1)
        print(f"\r{pct:5.1f}% done, {time.time() - t0:.0f}s elapsed", end="")
print("\nDone: transcript_en.txt")