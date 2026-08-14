# coding=utf-8
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
output = root / "build" / "datapack"

print("[pre_build] Cleaning output directory...")
if output.exists():
    shutil.rmtree(output)
print("[pre_build] Ready.")