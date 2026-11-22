import re
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "highlights.py"],
    capture_output=True, text=True, check=True,
)
print(result.stdout)

for m in re.finditer(r"best_(\d+)\.mp4: ([\d.]+)s to ([\d.]+)s", result.stdout):
    n, s, e = m.groups()
    subprocess.run(
        [sys.executable, "make_short.py", s, e, f"short_{n}_en.mp4", "transcript_en.txt"],
        check=True,
    )

print("All done")