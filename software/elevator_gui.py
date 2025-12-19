#!/usr/bin/env python3
"""
Elevator Controller GUI
A Tkinter-based graphical interface for the 4-floor elevator controller.
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import os
from verilog_interface import VerilogSimulator

class ElevatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Elevator Controller - 4 Floor Building")
        self.root.geometry("800x750")  # Made even taller
        self.root.resizable(True, True)  # Allow resizing
        
        # Elevator state variables
        self.current_floor = 0
        self.target_floor = 0
        self.is_moving = False
        self.direction = "up"  # "up" or "down"
        
        # Verilog simulation interface
        self.verilog_available = False
        self.setup_verilog_interface()
        
        # Debug: Print Verilog status
        print(f"DEBUG: Verilog available = {self.verilog_available}")
        
        # Colors and styling
        self.colors = {
            'bg': '#f0f0f0',
            'elevator_shaft': '#e0e0e0',
            'elevator_car': '#4CAF50',
            'button_normal': '#2196F3',
            'button_active': '#FF9800',
            'floor_active': '#FFC107'
        }
        
        self.setup_ui()
        
    def setup_verilog_interface(self):
        """Initialize Verilog simulation interface"""
        try:
            # Get paths relative to software directory
            software_dir = os.path.dirname(os.path.abspath(__file__))
            project_dir = os.path.dirname(software_dir)
            hardware_dir = os.path.join(project_dir, "hardware")
            simulation_dir = os.path.join(project_dir, "simulation")
            
            self.verilog_sim = VerilogSimulator(hardware_dir, simulation_dir)
            
            # Check if Verilog tools are available
            if self.verilog_sim.check_verilog_tools():
                self.verilog_available = True
                print("✓ Verilog simulation interface initialized")
            else:
                self.verilog_available = False
                print("ℹ Running in GUI-only mode (Verilog tools not available)")
                
        except Exception as e:
            print(f"Warning: Verilog interface initialization failed: {e}")
            self.verilog_available = False
        
    def setup_ui(self):
        """Initialize the user interface"""
        self.root.configure(bg=self.colors['bg'])
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="4-Floor Elevator Controller", 
            font=('Arial', 18, 'bold'),
            bg=self.colors['bg'],
            fg='#333'
        )
        title_label.pack(pady=(0, 20))
        
        # Create control frame and elevator frame
        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(expand=True, fill='both')
        
        # Left side - Control Panel
        self.create_control_panel(content_frame)
        
        # Right side - Elevator Visualization (placeholder for now)
        self.create_elevator_display(content_frame)
        
        # Status bar
        self.create_status_bar(main_frame)        
        # Initialize display
        self.update_display()
        
        # Start periodic updates for better visual feedback
        self.start_periodic_updates()        
    def create_control_panel(self, parent):
        """Create the control panel with floor buttons and status"""
        control_frame = tk.LabelFrame(
            parent, 
            text="Control Panel", 
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg'],
            fg='#333'
        )
        control_frame.pack(side=tk.LEFT, fill='y', padx=(0, 10))
        
        # Floor request buttons
        buttons_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        buttons_frame.pack(pady=20)
        
        tk.Label(
            buttons_frame, 
            text="Request Floor:", 
            font=('Arial', 11, 'bold'),
            bg=self.colors['bg']
        ).pack(pady=(0, 10))
        
        self.floor_buttons = []
        for floor in range(4):
            btn = tk.Button(
                buttons_frame,
                text=f"Floor {floor}",
                font=('Arial', 10, 'bold'),
                bg=self.colors['button_normal'],
                fg='white',
                width=12,
                height=2,
                command=lambda f=floor: self.request_floor(f)
            )
            btn.pack(pady=2)
            self.floor_buttons.append(btn)
            
        # Status display
        status_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        status_frame.pack(pady=20, fill='x')
        
        tk.Label(
            status_frame, 
            text="Status:", 
            font=('Arial', 11, 'bold'),
            bg=self.colors['bg']
        ).pack(anchor='w')
        
        self.status_labels = {}
        status_items = [
            ("Current Floor:", "current_floor"),
            ("Target Floor:", "target_floor"), 
            ("Moving:", "moving"),
            ("Direction:", "direction")
        ]
        
        for label_text, key in status_items:
            frame = tk.Frame(status_frame, bg=self.colors['bg'])
            frame.pack(fill='x', pady=2)
            
            tk.Label(
                frame, 
                text=label_text, 
                font=('Arial', 9),
                bg=self.colors['bg'],
                width=12,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            value_label = tk.Label(
                frame, 
                text="0", 
                font=('Arial', 9, 'bold'),
                bg=self.colors['bg'],
                anchor='w'
            )
            value_label.pack(side=tk.LEFT)
            self.status_labels[key] = value_label
            
        # Reset button
        reset_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        reset_frame.pack(pady=(20, 0))
        
        tk.Button(
            reset_frame,
            text="RESET",
            font=('Arial', 10, 'bold'),
            bg='#F44336',
            fg='white',
            width=12,
            height=2,
            command=self.reset_elevator
        ).pack()
        
        # Emergency stop button
        tk.Button(
            reset_frame,
            text="STOP",
            font=('Arial', 10, 'bold'),
            bg='#FF5722',
            fg='white',
            width=12,
            height=2,
            command=self.stop_elevator
        ).pack(pady=(5, 0))
        
        # Simulation mode toggle
        sim_frame = tk.LabelFrame(
            control_frame, 
            text="Simulation Mode",
            font=('Arial', 10, 'bold'),
            bg=self.colors['bg']
        )
        sim_frame.pack(pady=(10, 0), fill='x')
        
        self.sim_mode = tk.BooleanVar()
        self.sim_mode.set(self.verilog_available)
        
        sim_check = tk.Checkbutton(
            sim_frame,
            text="Use Verilog Hardware Simulation",
            variable=self.sim_mode,
            font=('Arial', 10, 'bold'),
            bg=self.colors['bg'],
            fg='#333',
            selectcolor='#4CAF50',
            state='normal' if self.verilog_available else 'disabled',
            command=self.on_simulation_mode_change
        )
        sim_check.pack(pady=10, padx=10, anchor='w')
        
        # Status label for simulation mode
        sim_status = "✅ Available" if self.verilog_available else "❌ Icarus Verilog not found"
        status_color = '#4CAF50' if self.verilog_available else '#F44336'
        
        tk.Label(
            sim_frame,
            text=f"Status: {sim_status}",
            font=('Arial', 9),
            bg=self.colors['bg'],
            fg=status_color
        ).pack(padx=10, anchor='w')
        
        # Debug: Print checkbox creation
        print(f"DEBUG: Checkbox created, Verilog available = {self.verilog_available}")
        
    def on_simulation_mode_change(self):
        """Handle simulation mode toggle"""
        if self.sim_mode.get():
            mode = "Verilog Hardware (step-by-step)"
            details = "Floor requests will use actual HDL simulation with clock cycles"
        else:
            mode = "GUI Animation (smooth)"
            details = "Floor requests will use smooth GUI animation"
            
        print(f"Simulation mode changed to: {mode}")
        self.status_text.config(text=f"Mode: {mode} - {details}")
        
    def create_elevator_display(self, parent):
        """Create the elevator shaft visualization"""
        display_frame = tk.LabelFrame(
            parent, 
            text="Elevator Shaft", 
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg'],
            fg='#333'
        )
        display_frame.pack(side=tk.RIGHT, expand=True, fill='both')
        
        # Canvas for elevator visualization
        self.canvas = tk.Canvas(
            display_frame,
            width=300,
            height=400,
            bg='white',
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.canvas.pack(padx=20, pady=20)
        
        # Initialize elevator visualization
        self.setup_elevator_shaft()
        
    def setup_elevator_shaft(self):
        """Draw the elevator shaft and floors"""
        # Clear canvas
        self.canvas.delete("all")
        
        # Shaft dimensions
        shaft_width = 120
        shaft_height = 320
        shaft_x = 90  # Center horizontally
        shaft_y = 40  # Start from top
        
        # Draw shaft walls
        self.canvas.create_rectangle(
            shaft_x, shaft_y, 
            shaft_x + shaft_width, shaft_y + shaft_height,
            fill=self.colors['elevator_shaft'],
            outline='#999',
            width=2
        )
        
        # Draw floor lines and labels
        floor_height = shaft_height // 4
        self.floor_positions = []
        
        for floor in range(4):
            # Calculate position (floor 0 at bottom, floor 3 at top)
            y_pos = shaft_y + shaft_height - (floor * floor_height) - floor_height
            self.floor_positions.append(y_pos)
            
            # Draw floor line
            self.canvas.create_line(
                shaft_x, y_pos + floor_height,
                shaft_x + shaft_width, y_pos + floor_height,
                fill='#666',
                width=2
            )
            
            # Floor number label (left side)
            self.canvas.create_text(
                shaft_x - 20, y_pos + floor_height // 2,
                text=f"F{3-floor}",  # Reverse order for display (F3 at top)
                font=('Arial', 12, 'bold'),
                fill='#333'
            )
            
            # Floor indicator light (right side)
            indicator_x = shaft_x + shaft_width + 20
            indicator_y = y_pos + floor_height // 2
            
            # Create floor indicator (will be updated based on current floor)
            color = self.colors['floor_active'] if (3-floor) == self.current_floor else '#ddd'
            self.canvas.create_oval(
                indicator_x - 8, indicator_y - 8,
                indicator_x + 8, indicator_y + 8,
                fill=color,
                outline='#999',
                width=2,
                tags=f"floor_indicator_{3-floor}"
            )
        
        # Draw elevator car
        self.draw_elevator_car()
        
        # Draw direction arrows
        self.draw_direction_arrows()
        
    def draw_elevator_car(self):
        """Draw the elevator car at current position"""
        # Remove existing elevator car
        self.canvas.delete("elevator_car")
        
        shaft_x = 90
        shaft_width = 120
        floor_height = 320 // 4
        shaft_y = 40
        
        # Calculate elevator position
        # Floor positions are stored with floor 0 at index 3, floor 3 at index 0
        floor_index = 3 - self.current_floor
        car_y = self.floor_positions[floor_index] + 10
        car_height = floor_height - 20
        car_width = shaft_width - 20
        car_x = shaft_x + 10
        
        # Draw elevator car
        self.canvas.create_rectangle(
            car_x, car_y,
            car_x + car_width, car_y + car_height,
            fill=self.colors['elevator_car'],
            outline='#2E7D32',
            width=2,
            tags="elevator_car"
        )
        
        # Draw elevator door
        door_width = car_width - 20
        door_height = car_height - 20
        door_x = car_x + 10
        door_y = car_y + 10
        
        self.canvas.create_rectangle(
            door_x, door_y,
            door_x + door_width, door_y + door_height,
            fill='#66BB6A',
            outline='#2E7D32',
            width=1,
            tags="elevator_car"
        )
        
        # Draw door split line
        self.canvas.create_line(
            door_x + door_width//2, door_y,
            door_x + door_width//2, door_y + door_height,
            fill='#2E7D32',
            width=2,
            tags="elevator_car"
        )
        
        # Current floor indicator inside elevator
        self.canvas.create_text(
            car_x + car_width//2, car_y + car_height//2,
            text=str(self.current_floor),
            font=('Arial', 24, 'bold'),
            fill='white',
            tags="elevator_car"
        )
        
    def draw_elevator_at_position(self, position):
        """Draw elevator at a specific position (for smooth animation)"""
        if not hasattr(self, 'canvas'):
            return
            
        # Remove existing elevator car
        self.canvas.delete("elevator_car")
        
        shaft_x = 90
        shaft_width = 120
        floor_height = 320 // 4
        shaft_y = 40
        
        # Calculate elevator position based on fractional floor position
        # Position 0.0 = floor 0, 1.5 = halfway between floor 1 and 2, etc.
        total_height = 320
        car_y = shaft_y + total_height - ((position + 1) * floor_height) + 10
        car_height = floor_height - 20
        car_width = shaft_width - 20
        car_x = shaft_x + 10
        
        # Draw elevator car
        self.canvas.create_rectangle(
            car_x, car_y,
            car_x + car_width, car_y + car_height,
            fill=self.colors['elevator_car'],
            outline='#2E7D32',
            width=2,
            tags="elevator_car"
        )
        
        # Draw elevator door
        door_width = car_width - 20
        door_height = car_height - 20
        door_x = car_x + 10
        door_y = car_y + 10
        
        self.canvas.create_rectangle(
            door_x, door_y,
            door_x + door_width, door_y + door_height,
            fill='#66BB6A',
            outline='#2E7D32',
            width=1,
            tags="elevator_car"
        )
        
        # Door split line
        self.canvas.create_line(
            door_x + door_width//2, door_y,
            door_x + door_width//2, door_y + door_height,
            fill='#2E7D32',
            width=2,
            tags="elevator_car"
        )
        
        # Floor number (show current floor or target if moving)
        display_floor = int(round(position))
        self.canvas.create_text(
            car_x + car_width//2, car_y + car_height//2,
            text=str(display_floor),
            font=('Arial', 24, 'bold'),
            fill='white',
            tags="elevator_car"
        )
        
    def draw_direction_arrows(self):
        """Draw direction arrows next to the elevator"""
        # Remove existing arrows
        self.canvas.delete("direction_arrow")
        
        if self.is_moving:
            shaft_x = 90
            shaft_width = 120
            arrow_x = shaft_x + shaft_width + 50
            
            # Find current elevator position
            floor_index = 3 - self.current_floor
            arrow_y = self.floor_positions[floor_index] + 40
            
            # Draw arrow based on direction
            if self.direction == "up":
                # Up arrow
                points = [
                    arrow_x, arrow_y - 10,      # Top point
                    arrow_x - 8, arrow_y + 2,  # Bottom left
                    arrow_x + 8, arrow_y + 2   # Bottom right
                ]
                color = '#4CAF50'
            else:
                # Down arrow  
                points = [
                    arrow_x, arrow_y + 10,      # Bottom point
                    arrow_x - 8, arrow_y - 2,  # Top left
                    arrow_x + 8, arrow_y - 2   # Top right
                ]
                color = '#FF9800'
                
            self.canvas.create_polygon(
                points,
                fill=color,
                outline='#333',
                width=2,
                tags="direction_arrow"
            )
        
    def create_status_bar(self, parent):
        """Create the bottom status bar"""
        status_bar = tk.Frame(parent, bg='#ddd', height=30)
        status_bar.pack(fill='x', side=tk.BOTTOM, pady=(10, 0))
        
        self.status_text = tk.Label(
            status_bar,
            text="System Ready - Select a floor to begin",
            font=('Arial', 9),
            bg='#ddd',
            anchor='w'
        )
        self.status_text.pack(side=tk.LEFT, padx=10, pady=5)
        
    def request_floor(self, floor):
        """Handle floor request"""
        if not self.is_moving and self.current_floor != floor:
            self.target_floor = floor
            
            if self.sim_mode.get() and self.verilog_available:
                # Use Verilog simulation
                self.request_floor_verilog(floor)
            else:
                # Use GUI animation
                self.request_floor_gui(floor)
                
        elif self.current_floor == floor:
            self.status_text.config(text=f"Already at floor {floor}")
        else:
            self.status_text.config(text="Elevator is moving, please wait...")
            
    def request_floor_verilog(self, floor):
        """Handle floor request using Verilog simulation"""
        self.status_text.config(text=f"Running Verilog simulation for floor {floor}...")
        self.is_moving = True
        self.update_display()
        
        # Run simulation in background thread to avoid GUI freezing
        def run_simulation():
            try:
                success, result = self.verilog_sim.simulate_elevator_request(
                    floor, self.current_floor
                )
                
                if success and result:
                    # Update GUI with simulation results
                    self.root.after(0, lambda: self.handle_verilog_result(result))
                else:
                    self.root.after(0, lambda: self.handle_verilog_error())
                    
            except Exception as e:
                print(f"Simulation thread error: {e}")
                self.root.after(0, lambda: self.handle_verilog_error())
                
        # Start simulation thread
        sim_thread = threading.Thread(target=run_simulation, daemon=True)
        sim_thread.start()
        
    def handle_verilog_result(self, result):
        """Handle Verilog simulation results with step-by-step animation"""
        if 'steps' in result and len(result['steps']) > 0:
            # Animate step by step based on Verilog simulation
            self.animate_verilog_steps(result['steps'], result)
        else:
            # Fallback to direct result
            self.current_floor = result.get('current_floor', self.target_floor)
            self.is_moving = result.get('moving', False)
            self.direction = result.get('direction', 'up')
            
            self.status_text.config(
                text=f"✓ Verilog simulation complete - Arrived at floor {self.current_floor}"
            )
            
            self.update_display()
            
        # Show simulation output in console
        if 'simulation_output' in result:
            print(f"Verilog simulation output:\n{result['simulation_output']}")
            
    def animate_verilog_steps(self, steps, final_result):
        """Animate elevator movement step by step based on Verilog simulation"""
        if not steps:
            return
            
        self.status_text.config(text="Playing back Verilog hardware simulation...")
        
        def animate_step(step_index):
            if step_index < len(steps):
                step = steps[step_index]
                
                # Update elevator state from Verilog step
                self.current_floor = step['floor']
                self.is_moving = step['moving']
                self.direction = step['direction']
                
                # Update status with step info
                step_info = f"Verilog Step {step_index + 1}: Floor {step['floor']}"
                if step['moving']:
                    step_info += f" (moving {step['direction']})"
                else:
                    step_info += " (stopped)"
                    
                self.status_text.config(text=step_info)
                
                # Update visual display
                self.update_display()
                
                # Schedule next step
                self.root.after(800, lambda: animate_step(step_index + 1))  # 800ms per step
            else:
                # Animation complete
                self.current_floor = final_result.get('current_floor', self.target_floor)
                self.is_moving = final_result.get('moving', False)
                self.direction = final_result.get('direction', 'up')
                
                self.status_text.config(
                    text=f"✓ Verilog simulation complete - Floor {self.current_floor} (Hardware verified)"
                )
                self.update_display()
        
        # Start the step-by-step animation
        animate_step(0)
            
    def handle_verilog_error(self):
        """Handle Verilog simulation errors"""
        self.is_moving = False
        self.status_text.config(text="Simulation error - falling back to GUI mode")
        self.sim_mode.set(False)
        self.update_display()
        
    def request_floor_gui(self, floor):
        """Handle floor request using GUI animation (original method)"""
        self.is_moving = True
        
        # Determine direction
        if self.current_floor < floor:
            self.direction = "up"
        else:
            self.direction = "down"
            
        self.status_text.config(text=f"Moving to floor {floor}...")
        self.update_display()
        
        # Start elevator movement animation
        self.move_elevator()
            
    def move_elevator(self):
        """Animate elevator movement"""
        if self.is_moving and self.current_floor != self.target_floor:
            # Move one floor
            if self.current_floor < self.target_floor:
                self.current_floor += 1
                self.direction = "up"
            else:
                self.current_floor -= 1 
                self.direction = "down"
                
            # Update status with floor info
            remaining_floors = abs(self.target_floor - self.current_floor)
            if remaining_floors > 0:
                self.status_text.config(
                    text=f"Floor {self.current_floor} - Moving {self.direction} to {self.target_floor} ({remaining_floors} floors remaining)"
                )
            else:
                self.status_text.config(text=f"Arriving at floor {self.current_floor}...")
                
            # Update display
            self.update_display()
            
            # Check if we've reached target
            if self.current_floor == self.target_floor:
                self.is_moving = False
                self.status_text.config(text=f"✓ Arrived at floor {self.current_floor} - Doors opening")
                self.update_display()
                
                # Simulate door opening delay
                self.root.after(1500, lambda: self.status_text.config(text="Ready for next request"))
            else:
                # Continue moving after delay (simulate elevator speed)
                self.root.after(1000, self.move_elevator)  # 1 second per floor
            
    def stop_elevator(self):
        """Emergency stop - stop elevator at current floor"""
        if self.is_moving:
            self.is_moving = False
            self.target_floor = self.current_floor
            self.status_text.config(text=f"Emergency stop at floor {self.current_floor}")
            self.update_display()
        else:
            self.status_text.config(text="Elevator is not moving")
            
    def reset_elevator(self):
        """Reset elevator to ground floor"""
        self.current_floor = 0
        self.target_floor = 0
        self.is_moving = False
        self.direction = "up"
        self.status_text.config(text="Elevator reset to ground floor")
        self.update_display()
        
    def update_display(self):
        """Update the status display and visual elements"""
        self.status_labels['current_floor'].config(text=str(self.current_floor))
        self.status_labels['target_floor'].config(text=str(self.target_floor))
        self.status_labels['moving'].config(text="Yes" if self.is_moving else "No")
        self.status_labels['direction'].config(text=self.direction.title())
        
        # Update button colors
        for i, btn in enumerate(self.floor_buttons):
            if i == self.current_floor and not self.is_moving:
                # Current floor - highlighted
                btn.config(bg=self.colors['floor_active'], state='disabled')
            elif i == self.target_floor and self.is_moving:
                # Target floor while moving - orange
                btn.config(bg=self.colors['button_active'], state='normal')
            else:
                # Normal floor button
                btn.config(bg=self.colors['button_normal'], state='normal')
                
        # Update floor indicators
        for floor in range(4):
            indicator_color = self.colors['floor_active'] if floor == self.current_floor else '#ddd'
            self.canvas.itemconfig(f"floor_indicator_{floor}", fill=indicator_color)
            
        # Redraw elevator car and arrows
        self.draw_elevator_car()
        self.draw_direction_arrows()
        
    def cleanup(self):
        """Cleanup resources when closing"""
        if hasattr(self, 'verilog_sim') and self.verilog_sim:
            self.verilog_sim.cleanup()
            
    def start_periodic_updates(self):
        """Start periodic UI updates for smooth animation"""
        self.update_status_bar_time()
        self.root.after(1000, self.start_periodic_updates)  # Update every second
        
    def update_status_bar_time(self):
        """Update status bar with current time"""
        current_time = time.strftime("%H:%M:%S")
        if hasattr(self, 'status_text'):
            current_status = self.status_text.cget('text')
            if not self.is_moving and 'Ready' not in current_status:
                self.status_text.config(text=f"Ready for requests - {current_time}")
                
    def animate_elevator_smooth(self, start_floor, end_floor):
        """Create smooth animation between floors"""
        if not hasattr(self, 'canvas'):
            return
            
        # Calculate animation steps
        steps = 20  # Number of animation frames
        floor_diff = end_floor - start_floor
        
        for step in range(steps + 1):
            progress = step / steps
            current_pos = start_floor + (floor_diff * progress)
            
            # Update elevator position smoothly
            self.root.after(
                step * 50,  # 50ms per frame
                lambda pos=current_pos: self.draw_elevator_at_position(pos)
            )

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = ElevatorGUI(root)
    
    # Handle window closing
    def on_closing():
        app.cleanup()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplication closed by user")
        app.cleanup()

if __name__ == "__main__":
    main()