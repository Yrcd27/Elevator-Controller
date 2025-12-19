#!/usr/bin/env python3
"""
Elevator Controller Testing Suite Launcher
Provides access to all testing modes and interfaces.
"""

import sys
import os
import subprocess

def print_banner():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║              ELEVATOR CONTROLLER TESTING SUITE               ║
║                                                               ║
║  Complete testing framework for Verilog HDL elevator        ║
║  controller with GUI integration and automated validation    ║
╚═══════════════════════════════════════════════════════════════╝
    """)

def main():
    print_banner()
    
    while True:
        print("\n🎯 Available Testing Options:")
        print("=" * 50)
        print("1. 🎮 Main GUI - Interactive elevator controller")
        print("2. 🧪 Manual Testing - GUI with Verilog validation")
        print("3. 🤖 Automated Testing - Comprehensive testbench suite")
        print("4. 🔧 Direct Verilog Test - Quick simulation verification")
        print("5. 📊 Full Test Suite - Run all tests sequentially")
        print("6. ❌ Exit")
        print("=" * 50)
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            print("\n🎮 Launching Main GUI...")
            try:
                subprocess.run(["python", "elevator_gui.py"])
            except Exception as e:
                print(f"Error: {e}")
                
        elif choice == "2":
            print("\n🧪 Launching Manual Testing Interface...")
            try:
                subprocess.run(["python", "manual_testing_gui.py"])
            except Exception as e:
                print(f"Error: {e}")
                
        elif choice == "3":
            print("\n🤖 Running Automated Test Suite...")
            try:
                subprocess.run(["python", "automated_verilog_tester.py"])
            except Exception as e:
                print(f"Error: {e}")
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            print("\n🔧 Running Direct Verilog Tests...")
            try:
                subprocess.run(["python", "test_verilog_only.py"])
            except Exception as e:
                print(f"Error: {e}")
            input("\nPress Enter to continue...")
            
        elif choice == "5":
            print("\n📊 Running Full Test Suite...")
            print("This will run all automated tests and generate a comprehensive report.")
            
            confirm = input("Continue? (y/N): ").lower().strip()
            if confirm in ['y', 'yes']:
                try:
                    print("\n1/3 - Running direct Verilog tests...")
                    subprocess.run(["python", "test_verilog_only.py"])
                    
                    print("\n2/3 - Running automated test suite...")
                    subprocess.run(["python", "automated_verilog_tester.py"])
                    
                    print("\n3/3 - Test suite complete!")
                    print("✅ All automated tests finished. Check output above for results.")
                    
                except Exception as e:
                    print(f"Error during full test suite: {e}")
                    
            input("\nPress Enter to continue...")
            
        elif choice == "6":
            print("\n👋 Thanks for using the Elevator Controller Testing Suite!")
            print("Your project is ready for demonstration and submission.")
            break
            
        else:
            print("❌ Invalid option. Please select 1-6.")

if __name__ == "__main__":
    # Change to software directory if needed
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main()