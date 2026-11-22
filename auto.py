import re
import shutil
import subprocess
import sys

if len(sys.argv) > 1:
    shutil.copy(sys.argv[1], "input.mp4")


def run(*args):
    subprocess.run([sys.executable, *args], check=True)


run("transcribe.py")
run("hinglish.py")

result = subprocess.run(
    [sys.executable, "highlights.py"],
    capture_output=True, text=True, check=True,
)
print(result.stdout)

for m in re.finditer(r"best_(\d+)\.mp4: ([\d.]+)s to ([\d.]+)s", result.stdout):
    n, s, e = m.groups()
    run("make_short.py", s, e, f"short_{n}_en.mp4", "transcript_en.txt")
    run("make_short.py", s, e, f"short_{n}_hinglish.mp4", "transcript_hi.txt")

print("All done")