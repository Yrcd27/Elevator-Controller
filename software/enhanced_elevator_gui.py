#!/usr/bin/env python3
"""
Enhanced Elevator GUI with Advanced Features
Final version with real-time updates, logging, and polish.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import os
from datetime import datetime
from verilog_interface import VerilogSimulator

class EnhancedElevatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Elevator Controller - 4 Floor Building")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Elevator state variables
        self.current_floor = 0
        self.target_floor = 0
        self.is_moving = False
        self.direction = "up"
        self.animation_speed = 1000  # milliseconds per floor
        
        # Statistics
        self.trips_completed = 0
        self.total_floors_traveled = 0
        
        # Verilog simulation interface
        self.verilog_available = False
        self.setup_verilog_interface()
        
        # Colors and styling
        self.colors = {
            'bg': '#f0f0f0',
            'elevator_shaft': '#e0e0e0',
            'elevator_car': '#4CAF50',
            'button_normal': '#2196F3',
            'button_active': '#FF9800',
            'floor_active': '#FFC107',
            'log_bg': '#2b2b2b',
            'log_fg': '#ffffff'
        }
        
        self.setup_ui()
        self.log_message("System initialized")
        
    def setup_verilog_interface(self):
        """Initialize Verilog simulation interface"""
        try:
            # Get paths relative to software directory
            software_dir = os.path.dirname(os.path.abspath(__file__))
            project_dir = os.path.dirname(software_dir)
            hardware_dir = os.path.join(project_dir, "hardware")
            simulation_dir = os.path.join(project_dir, "simulation")
            
            self.verilog_sim = VerilogSimulator(hardware_dir, simulation_dir)
            
            if self.verilog_sim.check_verilog_tools():
                self.verilog_available = True
                print("✓ Verilog simulation interface initialized")
            else:
                self.verilog_available = False
                print("ℹ Running in GUI-only mode")
                
        except Exception as e:
            print(f"Warning: Verilog interface initialization failed: {e}")
            self.verilog_available = False
            
    def setup_ui(self):
        """Initialize the enhanced user interface"""
        self.root.configure(bg=self.colors['bg'])
        
        # Create notebook for tabbed interface
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Main control tab
        main_frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(main_frame, text="Elevator Control")
        
        # Log tab
        log_frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(log_frame, text="System Log")
        
        # Statistics tab
        stats_frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(stats_frame, text="Statistics")
        
        # Setup each tab
        self.setup_main_tab(main_frame)
        self.setup_log_tab(log_frame)
        self.setup_stats_tab(stats_frame)
        
    def setup_main_tab(self, parent):
        """Setup the main control interface"""
        # Title
        title_label = tk.Label(
            parent, 
            text="4-Floor Elevator Controller", 
            font=('Arial', 18, 'bold'),
            bg=self.colors['bg'],
            fg='#333'
        )
        title_label.pack(pady=(10, 20))
        
        # Main content area
        content_frame = tk.Frame(parent, bg=self.colors['bg'])
        content_frame.pack(expand=True, fill='both', padx=20)
        
        # Left panel - Controls
        left_panel = tk.Frame(content_frame, bg=self.colors['bg'])
        left_panel.pack(side=tk.LEFT, fill='y', padx=(0, 20))
        
        self.create_control_panel(left_panel)
        
        # Right panel - Visualization
        right_panel = tk.Frame(content_frame, bg=self.colors['bg'])
        right_panel.pack(side=tk.RIGHT, expand=True, fill='both')
        
        self.create_elevator_display(right_panel)
        
        # Status bar
        self.create_status_bar(parent)
        
    def create_control_panel(self, parent):
        """Create enhanced control panel"""
        # Floor request section
        floor_frame = tk.LabelFrame(
            parent, 
            text="Floor Selection", 
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg']
        )
        floor_frame.pack(fill='x', pady=(0, 10))
        
        self.floor_buttons = []
        button_frame = tk.Frame(floor_frame, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        for floor in range(4):
            btn = tk.Button(
                button_frame,
                text=f"Floor {floor}",
                font=('Arial', 11, 'bold'),
                bg=self.colors['button_normal'],
                fg='white',
                width=10,
                height=2,
                command=lambda f=floor: self.request_floor(f)
            )
            btn.pack(pady=3)
            self.floor_buttons.append(btn)
            
        # Settings section
        settings_frame = tk.LabelFrame(
            parent, 
            text="Settings", 
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg']
        )
        settings_frame.pack(fill='x', pady=(0, 10))
        
        # Speed control
        speed_frame = tk.Frame(settings_frame, bg=self.colors['bg'])
        speed_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(speed_frame, text="Speed:", bg=self.colors['bg'], font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = tk.Scale(
            speed_frame, 
            from_=0.5, to=3.0, resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            bg=self.colors['bg'],
            command=self.update_speed
        )
        speed_scale.pack(side=tk.RIGHT, fill='x', expand=True)
        
        # Simulation mode
        sim_frame = tk.Frame(settings_frame, bg=self.colors['bg'])
        sim_frame.pack(fill='x', padx=10, pady=5)
        
        self.sim_mode = tk.BooleanVar(value=self.verilog_available)
        sim_check = tk.Checkbutton(
            sim_frame,
            text="Use Verilog Simulation",
            variable=self.sim_mode,
            bg=self.colors['bg'],
            state='normal' if self.verilog_available else 'disabled'
        )
        sim_check.pack(anchor='w')
        
        # Status section
        status_frame = tk.LabelFrame(
            parent, 
            text="Status", 
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg']
        )
        status_frame.pack(fill='x', pady=(0, 10))
        
        self.status_labels = {}
        status_items = [
            ("Current Floor:", "current_floor"),
            ("Target Floor:", "target_floor"),
            ("Moving:", "moving"),
            ("Direction:", "direction"),
            ("Trips:", "trips"),
        ]
        
        for label_text, key in status_items:
            frame = tk.Frame(status_frame, bg=self.colors['bg'])
            frame.pack(fill='x', padx=10, pady=2)
            
            tk.Label(
                frame, 
                text=label_text, 
                font=('Arial', 10),
                bg=self.colors['bg'],
                width=12,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            value_label = tk.Label(
                frame, 
                text="0", 
                font=('Arial', 10, 'bold'),
                bg=self.colors['bg'],
                anchor='w'
            )
            value_label.pack(side=tk.LEFT)
            self.status_labels[key] = value_label
            
        # Control buttons
        control_frame = tk.LabelFrame(
            parent, 
            text="Controls", 
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg']
        )
        control_frame.pack(fill='x')
        
        btn_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="STOP",
            font=('Arial', 10, 'bold'),
            bg='#FF5722',
            fg='white',
            width=12,
            command=self.stop_elevator
        ).pack(pady=2)
        
        tk.Button(
            btn_frame,
            text="RESET",
            font=('Arial', 10, 'bold'),
            bg='#F44336',
            fg='white',
            width=12,
            command=self.reset_elevator
        ).pack(pady=2)
        
    def create_elevator_display(self, parent):
        """Create enhanced elevator visualization"""
        display_frame = tk.LabelFrame(
            parent, 
            text="Elevator Shaft Visualization", 
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg']
        )
        display_frame.pack(expand=True, fill='both')
        
        # Canvas with scrollbar support
        canvas_frame = tk.Frame(display_frame, bg=self.colors['bg'])
        canvas_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            bg='white',
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.canvas.pack(expand=True, fill='both')
        
        self.setup_elevator_shaft()
        
    def setup_log_tab(self, parent):
        """Setup the system log tab"""
        log_label = tk.Label(
            parent,
            text="System Activity Log",
            font=('Arial', 14, 'bold'),
            bg=self.colors['bg']
        )
        log_label.pack(pady=(10, 5))
        
        # Log text area
        log_frame = tk.Frame(parent, bg=self.colors['bg'])
        log_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=20,
            bg=self.colors['log_bg'],
            fg=self.colors['log_fg'],
            insertbackground=self.colors['log_fg'],
            font=('Consolas', 10)
        )
        self.log_text.pack(expand=True, fill='both')
        
        # Clear log button
        clear_btn = tk.Button(
            parent,
            text="Clear Log",
            command=self.clear_log,
            bg='#666',
            fg='white'
        )
        clear_btn.pack(pady=(0, 10))
        
    def setup_stats_tab(self, parent):
        """Setup the statistics tab"""
        stats_label = tk.Label(
            parent,
            text="Elevator Statistics",
            font=('Arial', 14, 'bold'),
            bg=self.colors['bg']
        )
        stats_label.pack(pady=(10, 20))
        
        # Stats frame
        stats_content = tk.Frame(parent, bg=self.colors['bg'])
        stats_content.pack(expand=True, fill='both', padx=20)
        
        # Statistics labels
        self.stats_labels = {}
        stats_items = [
            ("Total Trips Completed:", "trips"),
            ("Total Floors Traveled:", "floors"),
            ("Average Trip Length:", "avg_trip"),
            ("Current Session Time:", "session_time"),
        ]
        
        for label_text, key in stats_items:
            frame = tk.Frame(stats_content, bg=self.colors['bg'])
            frame.pack(fill='x', pady=10)
            
            tk.Label(
                frame,
                text=label_text,
                font=('Arial', 12),
                bg=self.colors['bg'],
                width=20,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            value_label = tk.Label(
                frame,
                text="0",
                font=('Arial', 12, 'bold'),
                bg=self.colors['bg'],
                anchor='w'
            )
            value_label.pack(side=tk.LEFT)
            self.stats_labels[key] = value_label
            
        # Session start time
        self.session_start = datetime.now()
        
    def log_message(self, message):
        """Add message to system log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        if hasattr(self, 'log_text'):
            self.log_text.insert(tk.END, log_entry)
            self.log_text.see(tk.END)
            
    def clear_log(self):
        """Clear the system log"""
        if hasattr(self, 'log_text'):
            self.log_text.delete('1.0', tk.END)
            self.log_message("Log cleared")
            
    def update_speed(self, value):
        """Update animation speed"""
        self.animation_speed = int(2000 / float(value))  # Inverse relationship
        self.log_message(f"Speed set to {float(value):.1f}x")
        
    # [Continue with remaining methods from the original file...]
    # Note: This is a partial implementation showing the enhanced structure
    # The remaining methods (elevator visualization, movement, etc.) would follow