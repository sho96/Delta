import os
import subprocess as subp
import time
import sys

def compile_css():
    if os.name == "nt":
        subp.run(["./tools/compilecss"], shell=True)
    else:
        subp.run(["./tools/compilecss.sh"])
    