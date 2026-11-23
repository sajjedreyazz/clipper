import re, subprocess
from pathlib import Path

VIDEO = "input.mp4"
TRANSCRIPT = "transcript_en.txt"
MIN_LEN, MAX_LEN = 25, 60
N_SHORTS = 3
VERTICAL = True  # True = crop to 9:16 from the center

KEYWORDS = ["never", "secret", "solution", "problem", "mistake", "important",
            "why", "how", "best", "truth", "fluent", "confident", "practice",
            "learn", "first thing", "reason"]

BAD_START = re.compile(r'^(and|but|so|then|because|or|also|which|this|that|these|those|they|them|it|he|she|yeah|okay|well|right)\b', re.I)
pat = re.compile(r"\[([\d.]+) to ([\d.]+)\]\s*(.*)")
segs = []
for line in Path(TRANSCRIPT).read_text(encoding="utf-8", errors="ignore").splitlines():
    m = pat.match(line.strip())
    if m:
        segs.append((float(m[1]), float(m[2]), m[3].strip()))

# join lines into full sentences
sents, cur = [], []
for s in segs:
    cur.append(s)
    if re.search(r'[.?!]["\']?$', s[2]):
        sents.append(cur)
        cur = []
if cur:
    sents.append(cur)

def sstart(x): return x[0][0]
def send(x): return x[-1][1]
def stext(x): return " ".join(t[2] for t in x)

# candidate windows made of whole sentences
cands = []
for i in range(len(sents)):
    if len(stext(sents[i]).split()) < 4 or BAD_START.match(stext(sents[i])) or sstart(sents[i]) < 30:
        continue
    for j in range(i, len(sents)):
        dur = send(sents[j]) - sstart(sents[i])
        if dur > MAX_LEN:
            break
        if dur >= MIN_LEN:
            text = " ".join(stext(k) for k in sents[i:j + 1]).lower()
            score = len(text.split()) / dur * 10
            score += 3 * sum(text.count(k) for k in KEYWORDS)
            score -= 6 * text.count("?")
            score -= 8 * len(re.findall(r"(^|[.?!] )(yeah|okay|right|mm|um|uh|mhm)[.?!]", text))
            cands.append((score, sstart(sents[i]), send(sents[j])))

cands.sort(reverse=True)
picked = []
for sc, a, b in cands:
    if all(b <= pa or a >= pb for _, pa, pb in picked):
        picked.append((sc, a, b))
    if len(picked) == N_SHORTS:
        break
picked.sort(key=lambda x: x[1])

def ts(t):
    t = max(0, t)
    h, r = divmod(int(t * 1000), 3600000)
    m, r = divmod(r, 60000)
    s, ms = divmod(r, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

for n, (sc, a, b) in enumerate(picked, 1):
    t0, t1 = max(0, a - 0.2), b + 0.3
    srt = []
    k = 1
    for s0, s1, txt in segs:
        if s0 >= a - 0.05 and s1 <= b + 0.05:
            srt.append(f"{k}\n{ts(s0 - t0)} --> {ts(s1 - t0)}\n{txt}\n")
            k += 1
    Path(f"short_{n}.srt").write_text("\n".join(srt), encoding="utf-8")
    style = "FontSize=9,Bold=1,Outline=2,Alignment=2,MarginV=30"
    vf = f"subtitles=short_{n}.srt:force_style='FontName=Arial,FontSize=9,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=3,Alignment=2,MarginV=40'"
    if VERTICAL:
        vf = "crop=ih*9/16:ih,scale=720:1280," + vf
    out = f"final_{n}.mp4"
    print(f"\nShort {n}: {a:.1f}s to {b:.1f}s  ->  {out}")
    subprocess.run(["ffmpeg", "-y", "-ss", str(t0), "-i", VIDEO, "-t", str(t1 - t0),
                    "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "23", "-c:a", "aac", out], check=True)
print("\nAll done")









