#!/usr/bin/env python3
"""
Debug script to check Verilog integration status
"""

import sys
import os

# Add software directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Elevator Controller - Verilog Integration Debug")
print("=" * 50)

try:
    from verilog_interface import VerilogSimulator
    
    # Get paths
    software_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(software_dir)
    hardware_dir = os.path.join(project_dir, "hardware")
    simulation_dir = os.path.join(project_dir, "simulation")
    
    print(f"Software dir: {software_dir}")
    print(f"Project dir: {project_dir}")
    print(f"Hardware dir: {hardware_dir}")
    print(f"Simulation dir: {simulation_dir}")
    print()
    
    # Check if directories exist
    print("Directory checks:")
    print(f"✓ Hardware dir exists: {os.path.exists(hardware_dir)}")
    print(f"✓ Simulation dir exists: {os.path.exists(simulation_dir)}")
    print(f"✓ Verilog file exists: {os.path.exists(os.path.join(hardware_dir, 'elevator_controller.v'))}")
    print()
    
    # Create simulator
    simulator = VerilogSimulator(hardware_dir, simulation_dir)
    
    # Check Verilog tools
    print("Verilog tools check:")
    verilog_available = simulator.check_verilog_tools()
    print(f"Verilog available: {verilog_available}")
    print()
    
    if verilog_available:
        print("✅ Verilog integration should be ENABLED in GUI")
        print("   Look for: ☑ 'Use Verilog Simulation' checkbox")
    else:
        print("❌ Verilog integration will be DISABLED in GUI")
        print("   Checkbox will show as grayed out")
    
    print("\nIn the GUI, look for the checkbox:")
    print("- Location: Left panel, below STOP and RESET buttons")
    print("- Text: 'Use Verilog Simulation'")
    print("- Should be near the bottom of the control panel")
    
except Exception as e:
    print(f"Error during debug: {e}")
    import traceback
    traceback.print_exc()

input("\nPress Enter to exit...")