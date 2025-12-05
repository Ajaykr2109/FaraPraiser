#!/usr/bin/env python3
"""Startup script for FaraPraiser application."""

import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from farapraiser.main import main

if __name__ == "__main__":
    main()
