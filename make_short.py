import re
import subprocess
import sys
import textwrap

start = float(sys.argv[1])
end = float(sys.argv[2])
out = sys.argv[3]


def ts(t):
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return f"{h:02}:{m:02}:{s:06.3f}".replace(".", ",")


lines = []
n = 1
for line in open("transcript_en.txt", encoding="utf-8"):
    m = re.match(r"\[(\d+\.?\d*) to (\d+\.?\d*)\] (.*)", line)
    if not m:
        continue
    s, e, text = float(m[1]), float(m[2]), m[3]
    if e <= start or s >= end:
        continue
    s = max(s, start) - start
    e = min(e, end) - start
    wrapped = "\n".join(textwrap.wrap(text, 28))
    lines.append(f"{n}\n{ts(s)} --> {ts(e)}\n{wrapped}\n")
    n += 1

open("captions.srt", "w", encoding="utf-8").write("\n".join(lines))

vf = (
    "crop=ih*9/16:ih,scale=1080:1920,"
    "subtitles=captions.srt:force_style='FontSize=14,Alignment=2,MarginV=120,Outline=2'"
)
subprocess.run(
    ["ffmpeg", "-y", "-ss", str(start), "-i", "input.mp4",
     "-t", str(end - start), "-vf", vf,
     "-c:v", "libx264", "-c:a", "aac", out]
)
print("Done:", out)