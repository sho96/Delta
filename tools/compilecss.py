import os
import subprocess as subp
import time
import sys

NESTED_DIR = "css-nested"
TARGET_DIR = "css"

if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = os.listdir("css-nested")

start_time = time.perf_counter()
for filename in files:
    basename, ext = os.path.splitext(filename)
    print(f"compiling {basename}{ext}")
    if(os.name == "nt"):
        subp.run(["sass", f"{NESTED_DIR}/{filename}", f"{TARGET_DIR}/{basename}.css", "--no-source-map"], shell=True)
    else:
        subp.run(["sass", f"{NESTED_DIR}/{filename}", f"{TARGET_DIR}/{basename}.css", "--no-source-map"])

end_time = time.perf_counter()

print(f"compiled {len(files)} files in {round(end_time - start_time, 3)}s")