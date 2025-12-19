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
        
        # Placeholder for elevator visualization
        placeholder = tk.Label(
            display_frame,
            text="Elevator Visualization\n(Will be implemented in next task)",
            font=('Arial', 12),
            bg='#eeeeee',
            fg='#666',
            relief=tk.SUNKEN,
            borderwidth=2
        )
        placeholder.pack(expand=True, fill='both', padx=20, pady=20)
        
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
        """Update the status display"""
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

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = ElevatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()