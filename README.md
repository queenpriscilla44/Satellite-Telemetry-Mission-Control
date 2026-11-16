# Satellite Telemetry Simulator & Mission Control Dashboard

## Project Overview

The Satellite Telemetry Simulator is an educational project that simulates satellite sensor readings using C and displays the generated telemetry through a Python-based Streamlit dashboard.

The project demonstrates basic satellite telemetry generation, sensor validation, fault detection, data logging, and visualization.

**Note:** This is a software simulation. It does not connect to or receive data from a real satellite.

## Features

- C-based satellite telemetry generation
- Simulated temperature, battery voltage, current, altitude, and gyroscope readings
- Telemetry validation and fault detection
- CSV-based telemetry logging
- Live Streamlit dashboard
- Interactive sensor gauges and telemetry plots
- Satellite health monitoring
- Persistent alert history
- Simulated communication monitoring
- 3D Earth and satellite orbit visualization
- Historical telemetry analytics
- Telemetry and alert data export

## Technologies Used

- C
- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- CSV
- Visual Studio Code

## Project Structure

```text
Satellite_Telemetry_Simulator/
│
├── src/
│   ├── main.c
│   ├── sensors.c
│   ├── sensors.h
│   ├── telemetry.c
│   ├── telemetry.h
│   ├── fault_detection.c
│   ├── fault_detection.h
│   ├── health_monitor.c
│   ├── health_monitor.h
│   └── dashboard.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
[git clone YOUR_GITHUB_REPOSITORY_URL](https://github.com/queenpriscilla44/Satellite-Telemetry-Mission-Control.git)
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Compile the C simulator

Run this command from the project root:

```bash
gcc ./src/main.c ./src/sensors.c ./src/telemetry.c ./src/fault_detection.c ./src/health_monitor.c -o satellite.exe
```

### 4. Start the telemetry simulator

```bash
./satellite.exe
```

The simulator generates telemetry readings and saves them to a CSV file.

### 5. Launch the dashboard

Open a second terminal in the project root and run:

```bash
python -m streamlit run ./src/dashboard.py
```

The dashboard displays the generated telemetry and monitoring information.

## Project Applications

This project demonstrates concepts related to:

- Embedded C programming
- Sensor data acquisition and validation
- Telemetry monitoring
- Fault detection
- Data visualization
- Basic spacecraft health monitoring concepts

## Future Improvements

- Integration with hardware sensors or a microcontroller
- Real communication protocol implementation
- Improved telemetry storage and historical analysis
- Cloud-compatible telemetry simulation
- Deployment of the dashboard for public access

## Author

**Priscilla Queen S E**

Electronics and Communication Engineering  
Interest: Embedded Systems and Space Technology
