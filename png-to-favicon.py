#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

VENV_DIR = Path(".venv")
REQ = "pillow"

def venv_python() -> Path:
    # Return the Python executable path inside the virtual environment
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"

def ensure_venv_and_reexec():
    # If already running inside a virtual environment, do nothing
    if sys.prefix != sys.base_prefix:
        return

    py = venv_python()

    # 1) Create virtual environment if it does not exist
    if not py.exists():
        print("Creating virtual environment: .venv")
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])

    # 2) Install dependency if not available
    try:
        subprocess.check_call(
            [str(py), "-c", "import PIL"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print("📦 Installing Pillow inside venv...")
        subprocess.check_call([str(py), "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([str(py), "-m", "pip", "install", REQ])

    # 3) Re-execute the current script using the venv Python
    print("🔁 Re-executing script using venv Python...")
    os.execv(str(py), [str(py), *sys.argv])

def png_to_favicon(png_path: str, out_path: str = "favicon.ico"):
    from PIL import Image

    # Open PNG and convert to RGBA
    img = Image.open(png_path).convert("RGBA")

    # Define multiple icon sizes
    sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]

    # Save as ICO containing multiple resolutions
    img.save(out_path, format="ICO", sizes=sizes)

    print(f"Generated: {out_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 png_to_favicon.py input.png [output.ico]")
        sys.exit(1)

    input_png = sys.argv[1]
    output_ico = sys.argv[2] if len(sys.argv) >= 3 else "favicon.ico"
    png_to_favicon(input_png, output_ico)

if __name__ == "__main__":
    ensure_venv_and_reexec()
    main()
