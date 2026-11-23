import os
import shutil
import subprocess
import sys

if len(sys.argv) < 2:
    print("Usage: python run.py yourvideo.mp4")
    sys.exit(1)

if os.path.abspath(sys.argv[1]) != os.path.abspath("input.mp4"):
    shutil.copy(sys.argv[1], "input.mp4")

subprocess.run([sys.executable, "transcribe.py"], check=True)
subprocess.run([sys.executable, "shorts_en.py", sys.argv[2] if len(sys.argv) > 2 else "0"], check=True)
print("All done: see final_1.mp4, final_2.mp4, final_3.mp4")
