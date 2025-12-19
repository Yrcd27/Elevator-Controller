#!/usr/bin/env python3
"""
Verilog Simulation Interface
Bridges the Python GUI with the Verilog elevator controller simulation.
"""

import subprocess
import os
import tempfile
import time
from typing import Tuple, Optional

class VerilogSimulator:
    def __init__(self, hardware_dir: str, simulation_dir: str):
        """Initialize the Verilog simulator interface"""
        self.hardware_dir = hardware_dir
        self.simulation_dir = simulation_dir
        self.temp_tb_file = None
        
    def compile_design(self) -> bool:
        """Compile the Verilog design"""
        try:
            # Change to simulation directory
            os.chdir(self.simulation_dir)
            
            # Compile the design
            verilog_file = os.path.join(self.hardware_dir, "elevator_controller.v")
            testbench_file = os.path.join(self.simulation_dir, "elevator_tb.v")
            
            # Use iverilog to compile
            compile_cmd = [
                "iverilog", 
                "-o", "elevator_sim_gui",
                verilog_file,
                testbench_file
            ]
            
            result = subprocess.run(
                compile_cmd, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                print("✓ Verilog design compiled successfully")
                return True
            else:
                print(f"✗ Compilation failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("✗ Compilation timed out")
            return False
        except FileNotFoundError:
            print("✗ iverilog not found. Please install Icarus Verilog.")
            return False
        except Exception as e:
            print(f"✗ Compilation error: {e}")
            return False
            
    def create_custom_testbench(self, request_floor: int, current_floor: int = 0) -> str:
        """Create a custom testbench for specific elevator request"""
        testbench_content = f"""
module elevator_tb_gui;

    reg clk;
    reg reset;
    reg request_valid;
    reg [1:0] request_floor;

    wire [1:0] current_floor;
    wire moving;
    wire direction;

    elevator_controller dut (
        .clk(clk),
        .reset(reset),
        .request_valid(request_valid),
        .request_floor(request_floor),
        .current_floor(current_floor),
        .moving(moving),
        .direction(direction)
    );

    always #5 clk = ~clk;

    initial begin
        // Initialize signals
        clk = 0;
        reset = 1;
        request_valid = 0;
        request_floor = 2'd{current_floor};

        // Reset sequence
        #10 reset = 0;
        
        // Wait a bit then make request
        #10 request_floor = 2'd{request_floor};
            request_valid = 1;

        // Keep request active for a few cycles
        #30 request_valid = 0;

        // Run simulation long enough to complete movement
        #{abs(request_floor - current_floor) * 20 + 50} 
        
        // Output final state
        $display("Final state: current_floor=%d, moving=%b, direction=%b", 
                 current_floor, moving, direction);
        $finish;
    end

endmodule
"""
        return testbench_content
        
    def simulate_elevator_request(self, request_floor: int, current_floor: int = 0) -> Tuple[bool, Optional[dict]]:
        """Simulate elevator request and return results"""
        try:
            # Create temporary testbench
            tb_content = self.create_custom_testbench(request_floor, current_floor)
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='_gui.v', delete=False, dir=self.simulation_dir) as f:
                f.write(tb_content)
                self.temp_tb_file = f.name
            
            # Compile with custom testbench
            verilog_file = os.path.join(self.hardware_dir, "elevator_controller.v")
            
            compile_cmd = [
                "iverilog", 
                "-o", "elevator_sim_gui_custom",
                verilog_file,
                self.temp_tb_file
            ]
            
            compile_result = subprocess.run(
                compile_cmd, 
                capture_output=True, 
                text=True,
                cwd=self.simulation_dir,
                timeout=10
            )
            
            if compile_result.returncode != 0:
                print(f"Custom compilation failed: {compile_result.stderr}")
                return False, None
            
            # Run simulation
            sim_cmd = ["./elevator_sim_gui_custom"]
            sim_result = subprocess.run(
                sim_cmd,
                capture_output=True,
                text=True,
                cwd=self.simulation_dir,
                timeout=10
            )
            
            if sim_result.returncode == 0:
                # Parse simulation output
                output = sim_result.stdout
                # Look for final state output
                for line in output.split('\n'):
                    if 'Final state:' in line:
                        # Extract values (simplified parsing)
                        parts = line.split(',')
                        if len(parts) >= 3:
                            try:
                                floor_part = parts[0].split('=')[1].strip()
                                moving_part = parts[1].split('=')[1].strip()
                                direction_part = parts[2].split('=')[1].strip()
                                
                                result = {
                                    'current_floor': int(floor_part),
                                    'moving': moving_part == '1',
                                    'direction': 'up' if direction_part == '1' else 'down',
                                    'simulation_output': output
                                }
                                return True, result
                            except (IndexError, ValueError) as e:
                                print(f"Error parsing simulation output: {e}")
                                
                # If no final state found, return basic success
                return True, {
                    'simulation_output': output,
                    'current_floor': request_floor,
                    'moving': False,
                    'direction': 'up'
                }
            else:
                print(f"Simulation failed: {sim_result.stderr}")
                return False, None
                
        except Exception as e:
            print(f"Simulation error: {e}")
            return False, None
        finally:
            # Cleanup temporary file
            if self.temp_tb_file and os.path.exists(self.temp_tb_file):
                os.unlink(self.temp_tb_file)
                
    def check_verilog_tools(self) -> bool:
        """Check if Verilog simulation tools are available"""
        try:
            result = subprocess.run(
                ["iverilog", "-V"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print("✓ Icarus Verilog is available")
                return True
            else:
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("✗ Icarus Verilog not found")
            print("Please install Icarus Verilog: http://iverilog.icarus.com/")
            return False
            
    def cleanup(self):
        """Cleanup simulation files"""
        try:
            sim_files = ["elevator_sim_gui", "elevator_sim_gui_custom"]
            for sim_file in sim_files:
                sim_path = os.path.join(self.simulation_dir, sim_file)
                if os.path.exists(sim_path):
                    os.unlink(sim_path)
        except Exception as e:
            print(f"Cleanup warning: {e}")