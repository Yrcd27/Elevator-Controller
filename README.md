# Elevator Controller – Verilog HDL (4 Floors)

## Project Overview

This project implements a **simple elevator controller for a 4-floor building** using **Verilog HDL**.
The controller decides elevator movement based on a requested floor and the current floor.
Simulation and verification are done using **Icarus Verilog** and **GTKWave**.

This project is designed for **academic learning purposes** and demonstrates basic digital design concepts such as sequential logic and control logic.

---

## Features

* Supports **4 floors** (Floor 0 to Floor 3)
* One floor request at a time
* Elevator moves **one floor per clock cycle**
* Direction control (Up / Down)
* Reset functionality
* Fully simulated with waveform verification

---

## Tools Used

* **VS Code** – Code editor
* **Icarus Verilog** – Verilog compiler and simulator
* **GTKWave** – Waveform viewer
* **Windows OS**

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
│   └── (GUI implementation will be added here)
└── README.md                  # Project documentation
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
