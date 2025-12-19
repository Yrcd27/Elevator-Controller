#!/usr/bin/env python3
"""
Manual Testing Interface with GUI-Verilog Integration
Allows manual testing with automatic Verilog verification.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import sys
from datetime import datetime

# Add software directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from verilog_interface import VerilogSimulator
from automated_verilog_tester import AutomatedVerilogTester

class ManualTestingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Manual Testing with Verilog Validation")
        self.root.geometry("900x800")
        
        # Get project paths
        software_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_dir = os.path.dirname(software_dir)
        
        # Initialize Verilog interface
        self.verilog_sim = VerilogSimulator(
            os.path.join(self.project_dir, "hardware"),
            os.path.join(self.project_dir, "simulation")
        )
        
        # Initialize automated tester
        self.auto_tester = AutomatedVerilogTester(self.project_dir)
        
        # Test state
        self.current_floor = 0
        self.test_results = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the manual testing interface"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Manual testing tab
        manual_frame = tk.Frame(notebook)
        notebook.add(manual_frame, text="Manual Testing")
        
        # Automated testing tab
        auto_frame = tk.Frame(notebook)
        notebook.add(auto_frame, text="Automated Testing")
        
        # Results tab
        results_frame = tk.Frame(notebook)
        notebook.add(results_frame, text="Test Results")
        
        self.setup_manual_tab(manual_frame)
        self.setup_auto_tab(auto_frame)
        self.setup_results_tab(results_frame)
        
    def setup_manual_tab(self, parent):
        """Setup manual testing interface"""
        # Title
        tk.Label(
            parent,
            text="Manual Testing with Verilog Validation",
            font=('Arial', 16, 'bold')
        ).pack(pady=10)
        
        # Description
        desc_text = '''This interface allows you to manually test floor requests and automatically 
validates them against the Verilog implementation. Each test compares 
GUI simulation with actual hardware behavior.'''
        
        tk.Label(
            parent,
            text=desc_text,
            font=('Arial', 10),
            justify=tk.LEFT,
            wraplength=600
        ).pack(pady=10)
        
        # Current state display
        state_frame = tk.LabelFrame(parent, text="Current Elevator State", font=('Arial', 12, 'bold'))
        state_frame.pack(fill='x', padx=20, pady=10)
        
        self.state_label = tk.Label(
            state_frame,
            text=f"Current Floor: {self.current_floor}",
            font=('Arial', 14, 'bold'),
            fg='blue'
        )
        self.state_label.pack(pady=10)
        
        # Test controls
        control_frame = tk.LabelFrame(parent, text="Manual Test Controls", font=('Arial', 12, 'bold'))
        control_frame.pack(fill='x', padx=20, pady=10)
        
        # Floor selection
        tk.Label(control_frame, text="Select Target Floor:", font=('Arial', 11)).pack(pady=5)
        
        floor_frame = tk.Frame(control_frame)
        floor_frame.pack(pady=5)
        
        self.target_floor = tk.IntVar(value=1)
        for floor in range(4):
            tk.Radiobutton(
                floor_frame,
                text=f"Floor {floor}",
                variable=self.target_floor,
                value=floor,
                font=('Arial', 10)
            ).pack(side=tk.LEFT, padx=10)
            
        # Test button
        tk.Button(
            control_frame,
            text="🧪 Run Test with Verilog Validation",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            command=self.run_manual_test,
            height=2
        ).pack(pady=15)
        
        # Reset button
        tk.Button(
            control_frame,
            text="🔄 Reset to Floor 0",
            font=('Arial', 10),
            bg='#FF9800',
            fg='white',
            command=self.reset_elevator
        ).pack(pady=5)
        
        # Status display
        self.status_label = tk.Label(
            parent,
            text="Ready for testing. Select a floor and click 'Run Test'.",
            font=('Arial', 10),
            bg='#e8f5e8',
            relief=tk.SUNKEN,
            pady=5
        )
        self.status_label.pack(fill='x', padx=20, pady=10)
        
    def setup_auto_tab(self, parent):
        """Setup automated testing interface"""
        tk.Label(
            parent,
            text="Automated Verilog Testing",
            font=('Arial', 16, 'bold')
        ).pack(pady=20)
        
        desc_text = '''Run comprehensive automated tests on the Verilog elevator controller.
This will test all possible floor combinations and edge cases.'''
        
        tk.Label(
            parent,
            text=desc_text,
            font=('Arial', 10),
            justify=tk.CENTER,
            wraplength=600
        ).pack(pady=10)
        
        # Auto test button
        tk.Button(
            parent,
            text="🤖 Run Automated Test Suite",
            font=('Arial', 14, 'bold'),
            bg='#2196F3',
            fg='white',
            command=self.run_automated_tests,
            width=30,
            height=3
        ).pack(pady=30)
        
        # Progress display
        self.auto_progress = tk.Label(
            parent,
            text="Click 'Run Automated Test Suite' to begin comprehensive testing.",
            font=('Arial', 10),
            bg='#f0f0f0',
            relief=tk.SUNKEN,
            pady=10
        )
        self.auto_progress.pack(fill='x', padx=20, pady=10)
        
    def setup_results_tab(self, parent):
        """Setup test results display"""
        tk.Label(
            parent,
            text="Test Results History",
            font=('Arial', 16, 'bold')
        ).pack(pady=10)
        
        # Results text area
        results_frame = tk.Frame(parent)
        results_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Scrollable text widget
        from tkinter import scrolledtext
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=20,
            font=('Consolas', 9),
            bg='#f8f8f8'
        )
        self.results_text.pack(expand=True, fill='both')
        
        # Clear results button
        tk.Button(
            parent,
            text="Clear Results",
            command=self.clear_results,
            bg='#666',
            fg='white'
        ).pack(pady=10)
        
        self.log_result("System initialized. Ready for testing.")
        
    def run_manual_test(self):
        """Run manual test with Verilog validation"""
        target = self.target_floor.get()
        
        if self.current_floor == target:
            messagebox.showinfo("Test Result", f"Already at floor {target}. No movement needed.")
            return
            
        self.status_label.config(
            text=f"Testing: Floor {self.current_floor} → {target}. Running Verilog validation...",
            bg='#fff3cd'
        )
        
        # Run test in background thread
        def run_test():
            try:
                start_time = datetime.now()
                
                # Run Verilog simulation
                success, result = self.verilog_sim.simulate_elevator_request(target, self.current_floor)
                
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                if success:
                    # Update GUI state
                    old_floor = self.current_floor
                    self.current_floor = result['current_floor']
                    
                    # Update display
                    self.root.after(0, lambda: self.update_test_result(
                        old_floor, target, result, duration, True
                    ))
                else:
                    self.root.after(0, lambda: self.update_test_result(
                        self.current_floor, target, None, duration, False
                    ))
                    
            except Exception as e:
                self.root.after(0, lambda: self.handle_test_error(str(e)))
                
        # Start test thread
        test_thread = threading.Thread(target=run_test, daemon=True)
        test_thread.start()
        
    def update_test_result(self, old_floor, target_floor, result, duration, success):
        """Update GUI with test results"""
        if success:
            final_floor = result['current_floor']
            steps = result.get('steps', [])
            
            # Update state display
            self.state_label.config(text=f"Current Floor: {self.current_floor}")
            
            # Update status
            self.status_label.config(
                text=f"✓ Test completed! Moved {old_floor}→{final_floor} in {duration:.2f}s with {len(steps)} steps",
                bg='#d4edda'
            )
            
            # Log detailed results
            log_entry = f"""
📋 Manual Test: {datetime.now().strftime('%H:%M:%S')}
   Request: Floor {old_floor} → {target_floor}
   Result: Floor {final_floor}
   Duration: {duration:.2f} seconds
   Steps: {len(steps)}
   Status: {'✅ PASS' if final_floor == target_floor else '❌ FAIL'}
   Verilog Steps: {[f"F{s['floor']}" for s in steps]}
            """
            self.log_result(log_entry)
            
        else:
            self.status_label.config(
                text=f"❌ Test failed after {duration:.2f}s. Check Verilog implementation.",
                bg='#f8d7da'
            )
            
            log_entry = f"""
❌ Manual Test Failed: {datetime.now().strftime('%H:%M:%S')}
   Request: Floor {old_floor} → {target_floor}
   Duration: {duration:.2f} seconds
   Error: Verilog simulation failed
            """
            self.log_result(log_entry)
            
    def handle_test_error(self, error_msg):
        """Handle test errors"""
        self.status_label.config(
            text=f"❌ Test error: {error_msg}",
            bg='#f8d7da'
        )
        
        log_entry = f"""
💥 Test Error: {datetime.now().strftime('%H:%M:%S')}
   Error: {error_msg}
        """
        self.log_result(log_entry)
        
    def reset_elevator(self):
        """Reset elevator to floor 0"""
        self.current_floor = 0
        self.state_label.config(text=f"Current Floor: {self.current_floor}")
        self.status_label.config(
            text="Elevator reset to ground floor.",
            bg='#e8f5e8'
        )
        
        self.log_result(f"🔄 Elevator reset to Floor 0 at {datetime.now().strftime('%H:%M:%S')}")
        
    def run_automated_tests(self):
        """Run automated test suite"""
        self.auto_progress.config(
            text="🚀 Running automated test suite... This may take a minute.",
            bg='#cce5ff'
        )
        
        def run_tests():
            try:
                results = self.auto_tester.run_automated_tests()
                
                self.root.after(0, lambda: self.handle_auto_results(results))
                
            except Exception as e:
                self.root.after(0, lambda: self.handle_auto_error(str(e)))
                
        test_thread = threading.Thread(target=run_tests, daemon=True)
        test_thread.start()
        
    def handle_auto_results(self, results):
        """Handle automated test results"""
        if results["success"]:
            self.auto_progress.config(
                text=f"✅ All automated tests passed! {results['passed_tests']}/{results['total_tests']} tests successful.",
                bg='#d4edda'
            )
        else:
            failed = results.get('failed_tests', 0)
            total = results.get('total_tests', 0)
            self.auto_progress.config(
                text=f"❌ {failed} tests failed out of {total}. Check results for details.",
                bg='#f8d7da'
            )
            
        # Log detailed results
        log_entry = f"""
🤖 AUTOMATED TEST SUITE: {datetime.now().strftime('%H:%M:%S')}
{'='*50}
Total Tests: {results.get('total_tests', 'Unknown')}
Passed: {results.get('passed_tests', 'Unknown')}
Failed: {results.get('failed_tests', 'Unknown')}
Overall Result: {'✅ SUCCESS' if results['success'] else '❌ FAILURE'}

Detailed Output:
{results.get('output', 'No output available')}
{'='*50}
        """
        
        self.log_result(log_entry)
        
    def handle_auto_error(self, error_msg):
        """Handle automated test errors"""
        self.auto_progress.config(
            text=f"❌ Automated testing error: {error_msg}",
            bg='#f8d7da'
        )
        
        log_entry = f"""
💥 Automated Test Error: {datetime.now().strftime('%H:%M:%S')}
Error: {error_msg}
        """
        self.log_result(log_entry)
        
    def log_result(self, message):
        """Add message to results log"""
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)
        
    def clear_results(self):
        """Clear results log"""
        self.results_text.delete('1.0', tk.END)
        self.log_result("Results cleared.")

def main():
    """Run the manual testing GUI"""
    root = tk.Tk()
    app = ManualTestingGUI(root)
    
    def on_closing():
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()