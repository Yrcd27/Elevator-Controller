# Elevator Controller GUI

A Python Tkinter-based graphical interface for the 4-floor elevator controller Verilog project.

## Testing Framework

### **🏆 Comprehensive Testing Suite**

The project includes both manual and automated testing capabilities:

#### **Manual Testing (GUI-Based)**
- **Interface:** `manual_testing_gui.py`
- **Features:** Real-time Verilog validation, results logging, intuitive GUI
- **Use Case:** Interactive testing with immediate feedback

#### **Automated Testing (Verilog Testbench)**
- **Interface:** `automated_verilog_tester.py` 
- **Coverage:** 14 comprehensive test cases covering all floor combinations
- **Features:** Edge case testing, detailed Verilog testbench generation
- **Use Case:** Systematic validation and regression testing

#### **Test Cases Covered:**
1. **Basic Movement:** All floor-to-floor combinations (1→2, 1→3, 1→4, etc.)
2. **Edge Cases:** Same floor requests, multiple rapid requests
3. **Direction Changes:** Up-to-down and down-to-up transitions
4. **Boundary Testing:** Floor 1 and Floor 4 edge conditions
5. **Reset Functionality:** System reset during operation

#### **Testing Workflow:**
1. **Run Testing Launcher:** `python testing_launcher.py`
2. **Choose Testing Mode:** Manual GUI, Automated Suite, or Both
3. **Review Results:** Real-time feedback and detailed logs
4. **Verify Hardware:** All tests validate actual Verilog simulation

## Features

- **Interactive GUI** with elevator shaft visualization
- **Real-time animation** of elevator movement
- **Verilog simulation integration** (requires Icarus Verilog)
- **Floor request buttons** for floors 0-3
- **Status monitoring** with current floor, target, and direction
- **Control functions** including reset and emergency stop
- **Responsive design** with smooth animations

## Quick Start

### **🎯 Testing Suite Launcher (Recommended)**
```bash
cd software
python testing_launcher.py
```

This provides access to all testing modes:
- **Main GUI** - Interactive elevator controller
- **Manual Testing** - GUI with Verilog validation  
- **Automated Testing** - Comprehensive testbench suite
- **Direct Verilog Test** - Quick verification
- **Full Test Suite** - Complete validation

### **Individual Components**

1. **Main GUI:**
   ```bash
   python elevator_gui.py
   ```

2. **Manual Testing Interface:**
   ```bash
   python manual_testing_gui.py
   ```

3. **Automated Verilog Tests:**
   ```bash
   python automated_verilog_tester.py
   ```

4. **Quick Launcher:**
   ```bash
   python run_gui.py
   ```

## Requirements

### Python Requirements
- Python 3.6+ with tkinter (usually included)
- No additional Python packages required

### Optional: Verilog Simulation
For full hardware simulation integration:
- **Icarus Verilog** ([Download here](http://iverilog.icarus.com/))
  - Windows: Download installer from website
  - macOS: `brew install icarus-verilog`
  - Ubuntu/Debian: `sudo apt-get install iverilog`
  - CentOS/RHEL: `sudo yum install iverilog`

## File Structure

```
software/
├── elevator_gui.py          # Main GUI application
├── verilog_interface.py     # Verilog simulation bridge
├── run_gui.py              # Quick launcher script
├── test_suite.py           # Automated test suite
├── requirements.txt        # Dependencies documentation
└── README.md              # This file
```

## Usage

### Basic Operation

1. **Launch GUI:** Run `python run_gui.py`
2. **Select Floor:** Click any floor button (0-3)
3. **Watch Animation:** Elevator moves with visual feedback
4. **Monitor Status:** View current floor, direction, and moving state
5. **Control Options:** Use STOP for emergency or RESET to return to ground

### Verilog Simulation Mode

If Icarus Verilog is installed:
1. GUI automatically detects Verilog tools
2. Toggle "Use Verilog Simulation" checkbox
3. Floor requests will use actual Verilog hardware simulation
4. Results are integrated back into the GUI display

### Testing

Run the comprehensive test suite:
```bash
python test_suite.py
```

This includes:
- Automated Verilog interface tests
- Elevator logic validation
- Optional manual GUI testing

## GUI Components

### Main Interface
- **Elevator Shaft:** Visual representation with 4 floors
- **Elevator Car:** Animated car showing current position
- **Floor Indicators:** Lights showing current floor
- **Direction Arrows:** Show movement direction when active

### Control Panel
- **Floor Buttons:** Request specific floors (0-3)
- **Status Display:** Real-time elevator state information
- **Control Buttons:** STOP (emergency) and RESET functions
- **Settings:** Verilog simulation toggle

### Status Bar
- Real-time status messages
- Movement progress indicators
- System ready notifications

## Technical Details

### Animation System
- Smooth elevator movement between floors
- 1 second per floor travel time
- Visual feedback with direction arrows
- Floor indicator lights

### Verilog Integration
- Dynamic testbench generation
- Background simulation execution
- Thread-safe result handling
- Graceful fallback to GUI-only mode

### Error Handling
- Verilog compilation error detection
- Simulation timeout protection
- GUI responsiveness during simulations
- Automatic fallback mechanisms

## Troubleshooting

### Common Issues

**"Verilog tools not found"**
- Install Icarus Verilog from http://iverilog.icarus.com/
- Ensure `iverilog` is in your system PATH
- Restart the application after installation

**GUI doesn't start**
- Verify Python 3.6+ is installed
- Check that tkinter is available: `python -c "import tkinter"`
- On Linux: `sudo apt-get install python3-tk`

**Simulation fails**
- Check that hardware files exist in `../hardware/`
- Verify simulation directory `../simulation/` is accessible
- Try GUI-only mode (uncheck Verilog simulation)

### Performance

- GUI updates at 60 FPS for smooth animation
- Verilog simulations run in background threads
- Memory usage typically under 50MB
- CPU usage spikes briefly during simulations

## Development

### Extending the GUI

To add new features:

1. **New Controls:** Add to `create_control_panel()`
2. **Visualization:** Modify `create_elevator_display()`
3. **Simulation:** Extend `verilog_interface.py`
4. **Testing:** Add tests to `test_suite.py`

### Code Structure

- `ElevatorGUI`: Main application class
- `VerilogSimulator`: Hardware interface
- Event-driven architecture with tkinter mainloop
- Threaded simulation for responsiveness

## License

This project is for educational purposes. See main project README for details.

## Related Files

- `../hardware/elevator_controller.v` - Verilog hardware implementation
- `../simulation/elevator_tb.v` - Original testbench
- `../README.md` - Main project documentation