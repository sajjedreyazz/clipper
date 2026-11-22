import re
import subprocess

segs = []
for line in open("transcript_en.txt", encoding="utf-8"):
    m = re.match(r"\[(\d+\.?\d*) to (\d+\.?\d*)\] (.*)", line)
    if m:
        segs.append((float(m[1]), float(m[2]), m[3]))

WINDOW = 25
windows = []
for i in range(len(segs)):
    start = segs[i][0]
    end = start
    text = []
    for s in segs[i:]:
        if s[1] - start > WINDOW and text:
            break
        text.append(s[2])
        end = s[1]
    joined = " ".join(text)
    dur = max(end - start, 1)
    score = len(joined.split()) / dur + 0.5 * (joined.count("?") + joined.count("!"))
    windows.append((score, start, end, joined))

windows.sort(reverse=True)
chosen = []
for w in windows:
    if all(w[2] <= c[1] or w[1] >= c[2] for c in chosen):
        chosen.append(w)
    if len(chosen) == 3:
        break

for n, (score, start, end, text) in enumerate(chosen, 1):
    out = f"best_{n}.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-ss", str(start), "-i", "input.mp4",
         "-t", str(end - start), "-c:v", "libx264", "-c:a", "aac", out],
        capture_output=True,
    )
    print(f"{out}: {start:.1f}s to {end:.1f}s, score {score:.2f}")
    print("   ", text[:100])