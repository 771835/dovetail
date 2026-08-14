# coding=utf-8
from pathlib import Path

root = Path(__file__).resolve().parent.parent
output = root / "build" / "datapack"

print(f"[post_build] Build complete. Output at {output}")
if output.exists():
    for f in sorted(output.rglob("*")):
        print(f"  {f.relative_to(output)}")
else:
    print("  (no output)")