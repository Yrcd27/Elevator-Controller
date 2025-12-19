#!/usr/bin/env python3
"""
Quick launcher for the Elevator Controller GUI
"""

import sys
import os

# Add the software directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from elevator_gui import main
    main()
except ImportError as e:
    print(f"Error: {e}")
    print("Make sure you're running this from the software directory.")
except KeyboardInterrupt:
    print("\nGUI closed by user.")
except Exception as e:
    print(f"Unexpected error: {e}")