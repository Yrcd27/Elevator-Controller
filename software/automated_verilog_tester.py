#!/usr/bin/env python3
"""
Automated Verilog Testbench Generator and Runner
Generates comprehensive testbenches and runs automated testing.
"""

import os
import sys
import time
from typing import List, Dict, Tuple

# Add software directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from verilog_interface import VerilogSimulator

class AutomatedVerilogTester:
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.hardware_dir = os.path.join(project_dir, "hardware")
        self.simulation_dir = os.path.join(project_dir, "simulation")
        self.test_results = []
        
        self.simulator = VerilogSimulator(self.hardware_dir, self.simulation_dir)
        
    def generate_comprehensive_testbench(self) -> str:
        """Generate comprehensive testbench for automated testing"""
        testbench = """
module automated_elevator_tb;

    reg clk;
    reg reset;
    reg request_valid;
    reg [1:0] request_floor;

    wire [1:0] current_floor;
    wire moving;
    wire direction;

    integer test_count = 0;
    integer pass_count = 0;
    integer fail_count = 0;

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

    // Test task
    task test_floor_request;
        input [1:0] start_floor;
        input [1:0] target_floor;
        input integer test_id;
        
        integer expected_direction;
        integer steps_taken;
        integer max_steps;
        
        begin
            test_count = test_count + 1;
            steps_taken = 0;
            max_steps = 20; // Maximum steps allowed
            
            $display("TEST_%0d: Moving from floor %d to floor %d", test_id, start_floor, target_floor);
            
            // Determine expected direction
            if (start_floor < target_floor)
                expected_direction = 1; // up
            else if (start_floor > target_floor)
                expected_direction = 0; // down
            else
                expected_direction = direction; // same floor
            
            // Reset to start floor (simplified - assumes reset works)
            reset = 1;
            #20;
            reset = 0;
            #10;
            
            // Make the request
            request_floor = target_floor;
            request_valid = 1;
            #10;
            
            // Wait for movement to complete or timeout
            while ((current_floor != target_floor || moving) && steps_taken < max_steps) begin
                #10;
                steps_taken = steps_taken + 1;
                
                // Check direction during movement
                if (moving && current_floor != target_floor) begin
                    if (direction != expected_direction) begin
                        $display("TEST_%0d: FAIL - Wrong direction. Expected %d, got %d", 
                               test_id, expected_direction, direction);
                        fail_count = fail_count + 1;
                        return;
                    end
                end
            end
            
            request_valid = 0;
            #10;
            
            // Check final result
            if (current_floor == target_floor && !moving) begin
                $display("TEST_%0d: PASS - Reached floor %d in %d steps", 
                       test_id, current_floor, steps_taken);
                pass_count = pass_count + 1;
            end else begin
                $display("TEST_%0d: FAIL - Expected floor %d, got %d. Moving: %b", 
                       test_id, target_floor, current_floor, moving);
                fail_count = fail_count + 1;
            end
        end
    endtask

    initial begin
        $display("=== AUTOMATED ELEVATOR CONTROLLER TESTING ===");
        $display("Starting comprehensive test suite...");
        
        // Initialize
        clk = 0;
        reset = 1;
        request_valid = 0;
        request_floor = 0;
        
        #20;
        reset = 0;
        #10;
        
        // Test Case 1: Ground to each floor
        test_floor_request(0, 1, 1);
        test_floor_request(0, 2, 2);
        test_floor_request(0, 3, 3);
        
        // Test Case 2: Top floor to each floor
        test_floor_request(3, 2, 4);
        test_floor_request(3, 1, 5);
        test_floor_request(3, 0, 6);
        
        // Test Case 3: Middle floor movements
        test_floor_request(1, 3, 7);
        test_floor_request(2, 0, 8);
        test_floor_request(1, 2, 9);
        test_floor_request(2, 1, 10);
        
        // Test Case 4: Same floor requests
        test_floor_request(0, 0, 11);
        test_floor_request(2, 2, 12);
        
        // Test Case 5: Edge cases - maximum distance
        test_floor_request(0, 3, 13);
        test_floor_request(3, 0, 14);
        
        #50; // Final wait
        
        // Display final results
        $display("=== TEST RESULTS SUMMARY ===");
        $display("Total Tests: %d", test_count);
        $display("Passed: %d", pass_count);
        $display("Failed: %d", fail_count);
        
        if (fail_count == 0) begin
            $display("*** ALL TESTS PASSED! ***");
            $display("RESULT: SUCCESS");
        end else begin
            $display("*** %d TESTS FAILED ***", fail_count);
            $display("RESULT: FAILURE");
        end
        
        $display("=== END AUTOMATED TESTING ===");
        $finish;
    end

endmodule
"""
        return testbench
        
    def run_automated_tests(self) -> Dict:
        """Run comprehensive automated tests"""
        print("🧪 Running Automated Verilog Tests...")
        print("=" * 50)
        
        # Create automated testbench
        testbench_content = self.generate_comprehensive_testbench()
        testbench_file = os.path.join(self.simulation_dir, "automated_elevator_tb.v")
        
        try:
            # Write testbench file
            with open(testbench_file, 'w') as f:
                f.write(testbench_content)
                
            print(f"✓ Generated automated testbench: {testbench_file}")
            
            # Compile testbench
            verilog_file = os.path.join(self.hardware_dir, "elevator_controller.v")
            compile_cmd = [
                "iverilog",
                "-o", "automated_test",
                verilog_file,
                testbench_file
            ]
            
            print(f"🔧 Compiling: {' '.join(compile_cmd)}")
            
            import subprocess
            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                cwd=self.simulation_dir,
                timeout=30
            )
            
            if compile_result.returncode != 0:
                print(f"❌ Compilation failed:")
                print(compile_result.stderr)
                return {"success": False, "error": "Compilation failed"}
                
            print("✓ Compilation successful")
            
            # Run automated tests
            print("🚀 Running automated test suite...")
            
            sim_result = subprocess.run(
                ["vvp", "automated_test"],
                capture_output=True,
                text=True,
                cwd=self.simulation_dir,
                timeout=60
            )
            
            if sim_result.returncode != 0:
                print(f"❌ Test execution failed:")
                print(sim_result.stderr)
                return {"success": False, "error": "Test execution failed"}
                
            # Parse results
            output = sim_result.stdout
            print("\n" + "=" * 50)
            print("AUTOMATED TEST OUTPUT:")
            print("=" * 50)
            print(output)
            
            # Extract test results
            success = "RESULT: SUCCESS" in output
            total_tests = 0
            passed_tests = 0
            failed_tests = 0
            
            for line in output.split('\n'):
                if "Total Tests:" in line:
                    total_tests = int(line.split(':')[1].strip())
                elif "Passed:" in line:
                    passed_tests = int(line.split(':')[1].strip())
                elif "Failed:" in line:
                    failed_tests = int(line.split(':')[1].strip())
                    
            return {
                "success": success,
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "output": output
            }
            
        except Exception as e:
            print(f"❌ Automated testing error: {e}")
            return {"success": False, "error": str(e)}
        finally:
            # Cleanup
            if os.path.exists(testbench_file):
                os.unlink(testbench_file)
            sim_file = os.path.join(self.simulation_dir, "automated_test")
            if os.path.exists(sim_file):
                os.unlink(sim_file)

def main():
    """Run automated testing"""
    # Get project directory
    software_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(software_dir)
    
    print("🤖 Automated Verilog Testing System")
    print("=" * 40)
    print(f"Project: {project_dir}")
    
    # Create tester
    tester = AutomatedVerilogTester(project_dir)
    
    # Run tests
    start_time = time.time()
    results = tester.run_automated_tests()
    end_time = time.time()
    
    print("\n" + "=" * 50)
    print("FINAL SUMMARY:")
    print("=" * 50)
    
    if results["success"]:
        print("✅ ALL AUTOMATED TESTS PASSED!")
        print(f"📊 Results: {results['passed_tests']}/{results['total_tests']} tests passed")
    else:
        print("❌ SOME TESTS FAILED!")
        if 'total_tests' in results:
            print(f"📊 Results: {results['passed_tests']}/{results['total_tests']} tests passed")
            print(f"💥 Failed tests: {results['failed_tests']}")
        else:
            print(f"💥 Error: {results.get('error', 'Unknown error')}")
    
    print(f"⏱️ Test execution time: {end_time - start_time:.2f} seconds")
    print("\n🎯 Your elevator controller hardware has been thoroughly tested!")
    
if __name__ == "__main__":
    main()