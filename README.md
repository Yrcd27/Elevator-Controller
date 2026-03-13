<div align="center">

# Elevator Controller - Verilog HDL with Python GUI

A 4-floor elevator controller implemented in **Verilog HDL** with an integrated **Python (Tkinter) GUI**, featuring FSM-based control, simulation, and hardware-software integration.

[![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Verilog](https://img.shields.io/badge/Verilog-HDL-8A2BE2?style=flat)](https://en.wikipedia.org/wiki/Verilog)
[![Tkinter](https://img.shields.io/badge/Tkinter-GUI-FFB000?style=flat)](https://docs.python.org/3/library/tkinter.html)
[![Icarus%20Verilog](https://img.shields.io/badge/Icarus%20Verilog-Simulator-2C5AA0?style=flat)](http://iverilog.icarus.com/)
[![GTKWave](https://img.shields.io/badge/GTKWave-Waveform%20Viewer-4B8BBE?style=flat)](http://gtkwave.sourceforge.net/)

</div>

## Project Overview

This project implements a **complete elevator controller system for a 4-floor building** using **Verilog HDL** with an integrated **Python GUI interface**.
The system combines hardware description language design with modern graphical interface for demonstration and interaction.
Simulation and verification are done using **Icarus Verilog** and **GTKWave**, while the GUI provides real-time control and visualization.

This project is designed for **academic learning purposes** and demonstrates:
- Digital design concepts (sequential logic, control logic, finite state machines)
- Hardware-software integration
- GUI development with real-time visualization
- Simulation and testing methodologies

---

## Features

### Hardware (Verilog)
* Supports **4 floors** (Floor 0 to Floor 3)
* One floor request at a time
* Elevator moves **one floor per clock cycle**
* Direction control (Up / Down)
* Reset functionality
* Fully simulated with waveform verification

### Software (Python GUI)
* **Interactive graphical interface** with Tkinter
* **Real-time elevator visualization** with shaft and car animation
* **Floor request buttons** for intuitive control
* **Status monitoring** (current floor, direction, movement state)
* **Verilog simulation integration** (optional)
* **Control functions** (emergency stop, reset)
* **Responsive design** with smooth animations

---

## Tools Used

* **VS Code** – Code editor
* **Icarus Verilog** – Verilog compiler and simulator
* **GTKWave** – Waveform viewer
* **Python 3.6+** – GUI development
* **Tkinter** – GUI framework (included with Python)
* **Windows OS** (compatible with Linux/macOS)

All tools used are **free and open source**.

---

## Project Structure

```text
elevator_controller/
│
├── hardware/
│   └── elevator_controller.v   # Main elevator controller module
├── simulation/
│   ├── elevator_tb.v           # Testbench for simulation
│   ├── wave.vcd               # Waveform file (generated after simulation)
│   └── elevator_sim           # Compiled simulation executable
├── software/
│   ├── elevator_gui.py        # Main GUI application
│   ├── verilog_interface.py   # Verilog simulation bridge
│   ├── run_gui.py             # Quick launcher
│   ├── test_suite.py          # Automated tests
│   └── README.md              # GUI documentation
└── README.md                  # Project documentation (this file)
```

---

## Quick Start

### 1. Run the GUI Interface
```bash
cd software
python run_gui.py
```

### 2. Traditional Verilog Simulation
```bash
cd simulation
iverilog -o elevator_sim elevator_controller.v elevator_tb.v
./elevator_sim
gtkwave wave.vcd  # View waveforms
```

### 3. Run Tests
```bash
cd software
python test_suite.py
```

---

## Module Description

### Inputs

* `clk` : Clock signal
* `reset` : Asynchronous reset
* `request_valid` : Indicates a valid floor request
* `request_floor[1:0]` : Requested floor number (0–3)

### Outputs

* `current_floor[1:0]` : Current floor of the elevator
* `moving` : Indicates whether the elevator is moving
* `direction` : Elevator direction

  * `1` → Up
  * `0` → Down

---

## How the Elevator Works

1. On reset, the elevator starts at **Floor 0**.
2. When a valid floor request is given:

   * If requested floor > current floor → elevator moves up.
   * If requested floor < current floor → elevator moves down.
3. The elevator moves **one floor per clock cycle**.
4. When the requested floor is reached, the elevator stops.

---

## How to Run the Simulation

### Step 1: Open the project folder

Open the project folder in **VS Code**.

---

### Step 2: Compile the Verilog files

Open the VS Code terminal and run:

```bash
iverilog -o elevator_sim elevator_controller.v elevator_tb.v
```

---

### Step 3: Run the simulation

```bash
vvp elevator_sim
```

This will generate a waveform file named `wave.vcd`.

---

### Step 4: View the waveform

```bash
gtkwave wave.vcd
```

In GTKWave, add the following signals:

* `clk`
* `reset`
* `request_floor`
* `current_floor`
* `moving`
* `direction`

---

## Block-Level Design

The system consists of three main functional blocks:

1. **Request Interface** – Accepts floor request inputs
2. **Elevator Controller Logic** – Decides direction and movement
3. **Floor Register** – Stores and updates the current floor

These blocks work together synchronously using the clock signal.

---

## Simulation Output

The waveform confirms:

* Correct floor transitions
* Proper direction control
* Elevator stops at requested floors
* Reset behavior works as expected

---

## Limitations

* Only one request handled at a time
* No door control or timing logic
* No emergency handling

These limitations are intentional to keep the design simple and beginner-friendly.

---

## Author Notes

This project was created as part of an **HDL / Digital Design coursework** to understand:

* Verilog syntax
* Sequential logic
* Control logic
* Simulation and waveform analysis

---

## License

This project is for **educational use only**.
