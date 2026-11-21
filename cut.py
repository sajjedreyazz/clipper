import subprocess
import sys

start = sys.argv[1]
length = sys.argv[2]

subprocess.run([
    "ffmpeg", "-y",
    "-ss", start,
    "-i", "input.mp4",
    "-t", length,
    "-c:v", "libx264",
    "-c:a", "aac",
    "clip.mp4",
])
print("Done: clip.mp4 created")