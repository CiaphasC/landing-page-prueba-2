"""Optimize generated images for the NEXUS site.

Reads full-resolution images from C:/minimax/nexus-improved/images/src/ and writes
web-optimized variants to C:/minimax/nexus-improved/images/. Generates srcset sizes
that match the descriptors in index.html:
  - Projects (4:3):  800w, 1200w, 1920w
  - Portraits (1:1): 120w, 200w, 400w
"""
import os
from pathlib import Path
from PIL import Image

SRC = Path(r"C:\minimax\nexus-improved\images\src")
DST = Path(r"C:\minimax\nexus-improved\images")

PROJECTS = [
    "aura-cosmeticos.jpg",
    "nova-banking.jpg",
    "helio-studios.jpg",
]
PORTRAITS = [
    "maria-lopez.jpg",
    "andres-vega.jpg",
    "lucia-fernandez.jpg",
]

# (width, height) target for each srcset slot
PROJECT_SIZES = [(800, 600), (1200, 900), (1920, 1440)]
PORTRAIT_SIZES = [(120, 120), (200, 200), (400, 400)]

JPEG_QUALITY = 82


def optimize(src_name: str, sizes: list[tuple[int, int]]) -> list[tuple[str, int]]:
    src_path = SRC / src_name
    if not src_path.exists():
        return [(f"MISSING: {src_name}", 0)]
    img = Image.open(src_path).convert("RGB")
    results = []
    base = Path(src_name).stem
    for w, h in sizes:
        out = img.resize((w, h), Image.LANCZOS)
        out_name = f"{base}-{w}.jpg"
        out_path = DST / out_name
        out.save(out_path, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        results.append((out_name, out_path.stat().st_size))
    return results


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    SRC.mkdir(parents=True, exist_ok=True)
    total_in = 0
    total_out = 0
    print("=== Projects (4:3) ===")
    for name in PROJECTS:
        src_path = SRC / name
        if src_path.exists():
            total_in += src_path.stat().st_size
        for out_name, size in optimize(name, PROJECT_SIZES):
            total_out += size
            print(f"  {out_name:<32} {size:>9,} bytes")
    print("=== Portraits (1:1) ===")
    for name in PORTRAITS:
        src_path = SRC / name
        if src_path.exists():
            total_in += src_path.stat().st_size
        for out_name, size in optimize(name, PORTRAIT_SIZES):
            total_out += size
            print(f"  {out_name:<32} {size:>9,} bytes")
    print()
    print(f"Input  : {total_in / 1024 / 1024:6.2f} MB")
    print(f"Output : {total_out / 1024 / 1024:6.2f} MB")
    print(f"Saved  : {(total_in - total_out) / 1024 / 1024:6.2f} MB ({(1 - total_out / total_in) * 100:.1f}%)")


if __name__ == "__main__":
    main()
