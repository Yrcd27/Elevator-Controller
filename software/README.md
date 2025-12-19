# Elevator Controller GUI

A Python Tkinter-based graphical interface for the 4-floor elevator controller Verilog project.

## Features

- **Interactive GUI** with elevator shaft visualization
- **Real-time animation** of elevator movement
- **Verilog simulation integration** (requires Icarus Verilog)
- **Floor request buttons** for floors 0-3
- **Status monitoring** with current floor, target, and direction
- **Control functions** including reset and emergency stop
- **Responsive design** with smooth animations

## Quick Start

1. **Run the GUI:**
   ```bash
   cd software
   python run_gui.py
   ```

2. **Test the system:**
   ```bash
   python test_suite.py
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