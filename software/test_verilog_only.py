#!/usr/bin/env python3
"""
Test Verilog simulation directly
"""

import sys
import os

# Add software directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from verilog_interface import VerilogSimulator

def test_verilog_simulation():
    print("Testing Verilog Simulation...")
    print("=" * 40)
    
    # Setup paths
    software_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(software_dir)
    hardware_dir = os.path.join(project_dir, "hardware")
    simulation_dir = os.path.join(project_dir, "simulation")
    
    print(f"Hardware dir: {hardware_dir}")
    print(f"Simulation dir: {simulation_dir}")
    
    # Check files exist
    verilog_file = os.path.join(hardware_dir, "elevator_controller.v")
    print(f"Verilog file exists: {os.path.exists(verilog_file)}")
    
    if not os.path.exists(verilog_file):
        print("ERROR: elevator_controller.v not found!")
        return
        
    # Create simulator
    simulator = VerilogSimulator(hardware_dir, simulation_dir)
    
    # Test simulation
    print("\nTesting floor request: 0 → 2")
    success, result = simulator.simulate_elevator_request(2, 0)
    
    if success:
        print("✓ Simulation successful!")
        print(f"Result: {result}")
    else:
        print("✗ Simulation failed!")
        
    print("\nTesting floor request: 3 → 1")  
    success, result = simulator.simulate_elevator_request(1, 3)
    
    if success:
        print("✓ Simulation successful!")
        print(f"Result: {result}")
    else:
        print("✗ Simulation failed!")

if __name__ == "__main__":
    test_verilog_simulation()
    input("\nPress Enter to exit...")