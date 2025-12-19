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
        """Create a custom testbench for specific elevator request with step tracking"""
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

    // Track previous floor to detect changes
    reg [1:0] prev_floor;
    
    initial begin
        // Initialize signals
        clk = 0;
        reset = 1;
        request_valid = 0;
        request_floor = 2'd{current_floor};
        prev_floor = 2'd{current_floor};

        // Reset sequence
        #10 reset = 0;
        
        // Wait a bit then make request
        #10 request_floor = 2'd{request_floor};
            request_valid = 1;
            $display("STEP: floor=%d, moving=%b, direction=%b, target={request_floor}", 
                     current_floor, moving, direction);

        // Monitor floor changes during movement
        repeat(50) begin
            #10;
            if (prev_floor != current_floor || moving) begin
                $display("STEP: floor=%d, moving=%b, direction=%b", 
                         current_floor, moving, direction);
                prev_floor = current_floor;
            end
            
            // Stop when elevator reaches target and stops moving
            if (!moving && current_floor == 2'd{request_floor}) begin
                #10; // Wait one more cycle
                $display("FINAL: floor=%d, moving=%b, direction=%b", 
                         current_floor, moving, direction);
                $finish;
            end
        end
        
        // Fallback finish
        $display("FINAL: floor=%d, moving=%b, direction=%b", 
                 current_floor, moving, direction);
        $finish;
    end

endmodule
"""
        return testbench_content
        
    def simulate_elevator_request(self, request_floor: int, current_floor: int = 0) -> Tuple[bool, Optional[dict]]:
        """Simulate elevator request and return results"""
        print(f"Starting Verilog simulation: {current_floor} → {request_floor}")
        
        try:
            # Create temporary testbench
            tb_content = self.create_custom_testbench(request_floor, current_floor)
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='_gui.v', delete=False, dir=self.simulation_dir) as f:
                f.write(tb_content)
                self.temp_tb_file = f.name
            
            print(f"Created testbench: {self.temp_tb_file}")
            
            # Compile with custom testbench
            verilog_file = os.path.join(self.hardware_dir, "elevator_controller.v")
            
            # Run simulation - use vvp (Verilog runtime) instead of direct executable
            sim_executable_name = "elevator_sim_gui_custom"  # No .exe extension
            
            compile_cmd = [
                "iverilog", 
                "-o", sim_executable_name,
                verilog_file,
                self.temp_tb_file
            ]
            
            print(f"Compiling: {' '.join(compile_cmd)}")
            
            compile_result = subprocess.run(
                compile_cmd, 
                capture_output=True, 
                text=True,
                cwd=self.simulation_dir,
                timeout=15
            )
            
            if compile_result.returncode != 0:
                print(f"✗ Compilation failed:")
                print(f"  Error: {compile_result.stderr}")
                print(f"  Command: {' '.join(compile_cmd)}")
                return False, None
                
            print("✓ Compilation successful")
            
            # Run simulation using vvp (Verilog runtime) - this works better on Windows
            sim_file = os.path.join(self.simulation_dir, sim_executable_name)
            sim_cmd = ["vvp", sim_file]
            
            print(f"Running simulation: {' '.join(sim_cmd)}")
            
            sim_result = subprocess.run(
                sim_cmd,
                capture_output=True,
                text=True,
                cwd=self.simulation_dir,
                timeout=15
            )
            
            print(f"Simulation exit code: {sim_result.returncode}")
            print(f"Simulation output: {sim_result.stdout}")
            if sim_result.stderr:
                print(f"Simulation errors: {sim_result.stderr}")
            
            if sim_result.returncode == 0:
                # Parse simulation output for step-by-step movement
                output = sim_result.stdout
                print(f"Parsing output: {output}")
                
                # Extract all step information
                steps = []
                final_result = None
                
                for line in output.split('\n'):
                    line = line.strip()
                    if line.startswith('STEP:'):
                        # Parse step: "STEP: floor=1, moving=1, direction=1"
                        try:
                            parts = line.replace('STEP:', '').strip().split(',')
                            floor_part = parts[0].split('=')[1].strip()
                            moving_part = parts[1].split('=')[1].strip()
                            direction_part = parts[2].split('=')[1].strip()
                            
                            step_info = {
                                'floor': int(floor_part),
                                'moving': moving_part == '1',
                                'direction': 'up' if direction_part == '1' else 'down'
                            }
                            steps.append(step_info)
                            print(f"Step parsed: {step_info}")
                        except Exception as e:
                            print(f"Error parsing step: {line}, error: {e}")
                            
                    elif line.startswith('FINAL:'):
                        # Parse final state
                        try:
                            parts = line.replace('FINAL:', '').strip().split(',')
                            floor_part = parts[0].split('=')[1].strip()
                            moving_part = parts[1].split('=')[1].strip()
                            direction_part = parts[2].split('=')[1].strip()
                            
                            final_result = {
                                'current_floor': int(floor_part),
                                'moving': moving_part == '1',
                                'direction': 'up' if direction_part == '1' else 'down',
                                'simulation_output': output,
                                'steps': steps  # Include step-by-step data
                            }
                            print(f"Final result: {final_result}")
                        except Exception as e:
                            print(f"Error parsing final: {line}, error: {e}")
                
                if final_result:
                    return True, final_result
                elif steps:
                    # If no final but we have steps, use last step
                    last_step = steps[-1]
                    result = {
                        'current_floor': last_step['floor'],
                        'moving': last_step['moving'],
                        'direction': last_step['direction'],
                        'simulation_output': output,
                        'steps': steps
                    }
                    return True, result
                else:
                    # Fallback - no structured output found
                    result = {
                        'simulation_output': output,
                        'current_floor': request_floor,
                        'moving': False,
                        'direction': 'up',
                        'steps': []
                    }
                    print(f"✓ Simulation completed (fallback): {result}")
                    return True, result
            else:
                print(f"✗ Simulation failed with exit code {sim_result.returncode}")
                print(f"  stdout: {sim_result.stdout}")
                print(f"  stderr: {sim_result.stderr}")
                return False, None
                
        except Exception as e:
            print(f"✗ Simulation error: {e}")
            import traceback
            traceback.print_exc()
            return False, None
        finally:
            # Cleanup temporary file
            if self.temp_tb_file and os.path.exists(self.temp_tb_file):
                try:
                    os.unlink(self.temp_tb_file)
                    print(f"Cleaned up: {self.temp_tb_file}")
                except Exception as e:
                    print(f"Cleanup warning: {e}")
                
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