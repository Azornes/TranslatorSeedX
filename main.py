#!/usr/bin/env python3
"""
Main entry point for Seed-X Translation Application
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.gui.translator_app import main

if __name__ == "__main__":
    main()
