import glob
import os
import shutil
import subprocess
import sys
import time

EXT = (".mp4", ".mkv", ".mov", ".webm")
for d in ("inbox", "outbox", os.path.join("inbox", "done")):
    os.makedirs(d, exist_ok=True)


def stable(path):
    size = os.path.getsize(path)
    time.sleep(5)
    return size == os.path.getsize(path)


print("Watching the 'inbox' folder. Press Ctrl+C to stop.")
while True:
    for name in os.listdir("inbox"):
        path = os.path.join("inbox", name)
        if not name.lower().endswith(EXT) or not os.path.isfile(path):
            continue
        if not stable(path):
            continue
        print("Processing", name)
        for old in glob.glob("final_*.mp4"):
            os.remove(old)
        result = subprocess.run([sys.executable, "run.py", path])
        done = os.path.join("inbox", "done")
        if result.returncode == 0:
            out = os.path.join("outbox", os.path.splitext(name)[0])
            os.makedirs(out, exist_ok=True)
            for f in glob.glob("final_*.mp4"):
                shutil.move(f, out)
            shutil.move(path, os.path.join(done, name))
            print("Done, clips are in", out)
        else:
            shutil.move(path, os.path.join(done, "FAILED_" + name))
            print("Failed on", name)
    time.sleep(10)