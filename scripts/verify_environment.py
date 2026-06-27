#!/usr/bin/env python3
"""
scripts/verify_environment.py
=============================
Validation utility for the Fractal project workspace.
Checks python dependencies, submodule initialization, and environment keys.
"""

from __future__ import annotations

import os
import sys
import urllib.request
from pathlib import Path

def check_python_version() -> bool:
    print(f"[*] Checking Python Version... {sys.version.split()[0]}", end=" ")
    if sys.version_info >= (3, 10):
        print("[OK]")
        return True
    else:
        print("[FAILED] (Requires Python 3.10+)")
        return False

def check_submodules() -> bool:
    print("[*] Verifying Submodule Status...", end=" ")
    missing = []
    
    submodules = {
        "FractalCore": "FractalCore/requirements.txt",
        "FractalAndroid": "FractalApp/FractalAndroid/build.gradle.kts"
    }
    
    for name, marker in submodules.items():
        path = Path(marker)
        if not path.exists():
            missing.append(name)
            
    if missing:
        print(f"[FAILED] (Missing: {', '.join(missing)})")
        print("    -> Run 'git submodule update --init --recursive'")
        return False
    else:
        print("[OK]")
        return True

def check_env_files() -> bool:
    print("[*] Verifying Configuration Envs...", end=" ")
    private_env = Path("private.envs/Fractal/restore.ps1")
    if not private_env.exists():
        print("[WARNING] (Private submodules or keys are not restored)")
        print("    -> Note: Restoring local configs will require running restore.ps1")
        return False
    print("[OK]")
    return True

def check_huggingface_connection() -> bool:
    print("[*] Verifying Hugging Face Connection...", end=" ")
    try:
        # Check connection to Hugging Face
        urllib.request.urlopen("https://huggingface.co", timeout=5)
        print("[OK]")
        return True
    except Exception:
        print("[WARNING] (Could not connect to huggingface.co)")
        print("    -> Check your network proxy or internet settings.")
        return False

def main():
    print("=========================================")
    print("      FRACTAL ENVIRONMENT VALIDATOR      ")
    print("=========================================")
    
    success = True
    success &= check_python_version()
    success &= check_submodules()
    check_env_files() # Non-blocking warning
    check_huggingface_connection() # Non-blocking warning
    
    print("=========================================")
    if success:
        print("[SUCCESS] Environment verification passed.")
        sys.exit(0)
    else:
        print("[ERROR] Environment verification failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
