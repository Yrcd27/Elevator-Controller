#!/usr/bin/env python3
"""
Elevator Controller GUI
A Tkinter-based graphical interface for the 4-floor elevator controller.
"""

import tkinter as tk
from tkinter import ttk
import threading
import time

class ElevatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Elevator Controller - 4 Floor Building")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Elevator state variables
        self.current_floor = 0
        self.target_floor = 0
        self.is_moving = False
        self.direction = "up"  # "up" or "down"
        
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
        tk.Button(
            control_frame,
            text="RESET",
            font=('Arial', 10, 'bold'),
            bg='#F44336',
            fg='white',
            width=12,
            height=2,
            command=self.reset_elevator
        ).pack(pady=(20, 0))
        
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
        if not self.is_moving:
            self.target_floor = floor
            self.status_text.config(text=f"Floor {floor} requested...")
            self.update_display()
            # TODO: In next task, implement actual elevator movement
            print(f"Floor {floor} requested")
        else:
            self.status_text.config(text="Elevator is moving, please wait...")
            
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
            if i == self.current_floor:
                btn.config(bg=self.colors['floor_active'])
            else:
                btn.config(bg=self.colors['button_normal'])
                
        # Update floor indicators
        for floor in range(4):
            indicator_color = self.colors['floor_active'] if floor == self.current_floor else '#ddd'
            self.canvas.itemconfig(f"floor_indicator_{floor}", fill=indicator_color)
            
        # Redraw elevator car and arrows
        self.draw_elevator_car()
        self.draw_direction_arrows()

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = ElevatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()