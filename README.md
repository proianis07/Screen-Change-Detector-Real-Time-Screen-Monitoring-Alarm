# Screen Change Detector

A Python-based real-time screen monitoring system that detects visual changes using OpenCV and triggers an audible alarm when activity exceeds a configurable threshold.

## Overview

Screen Change Detector is a lightweight monitoring tool designed to detect changes occurring on your computer screen.

The program continuously captures screenshots, processes them using OpenCV, and compares consecutive frames to identify visual changes.

When detected changes exceed a configurable threshold, an audible alarm is activated.

The project uses Python's threading capabilities to handle keyboard input independently from the main monitoring loop.

## Features

- **Real-time screen monitoring:** Continuously captures the primary monitor.
- **Visual change detection:** Uses OpenCV to compare consecutive grayscale frames.
- **Configurable sensitivity:** Adjusts how much pixel-level change is required to register activity.
- **Percentage-based detection:** Triggers the alarm when the percentage of changed pixels exceeds a specified threshold.
- **Audible alarm:** Includes a built-in `alarm.wav` sound that plays continuously when triggered.
- **Keyboard controls:** Enable, disable, or silence the monitoring system without closing the program.
- **Lightweight processing:** Uses NumPy and OpenCV for image processing.

## Technologies Used

| Library | Purpose |
|---|---|
| Python | Main programming language |
| OpenCV | Image processing and frame comparison |
| MSS | Screen capture |
| NumPy | Image data processing |
| Pygame | Audio playback |
| Pynput | Keyboard input monitoring |
| Threading | Independent keyboard event handling |

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/proianis07/screen-movement-detector.git
```

### 2. Navigate to the project directory

```bash
cd screen-movement-detector
```

### 3. Install dependencies

```bash
pip install opencv-python mss numpy pygame pynput
```

### 4. Run the program

The repository already includes `alarm.wav`. No additional audio files are required.

Make sure `alarm.wav` is located in the same directory as `main.py`.

```bash
python main.py
```

## Keyboard Controls

| Key | Function |
|---|---|
| F8 | Enable monitoring |
| F9 | Disable monitoring |
| SPACE | Silence the alarm |
| CTRL + C | Exit the program |

## Configuration

The detection system can be customized by modifying the following parameters in `main.py`:

```python
CAPTURE_INTERVAL = 0.2
CHANGE_THRESHOLD = 1.5
PIXEL_SENSITIVITY = 35
ALARM_FILE = "alarm.wav"
```

- `CAPTURE_INTERVAL`: Time interval between consecutive screen captures, in seconds.
- `CHANGE_THRESHOLD`: Minimum percentage of changed pixels required to trigger the alarm.
- `PIXEL_SENSITIVITY`: Minimum grayscale pixel difference required for a pixel to be considered changed.
- `ALARM_FILE`: Path to the audio file used for the alarm.

## How It Works

The detection process follows several steps:

1. **Screen Capture:** MSS captures the primary monitor.
2. **Grayscale Conversion:** OpenCV converts the captured image into grayscale.
3. **Frame Comparison:** Consecutive frames are compared using absolute pixel differences.
4. **Thresholding:** Pixel differences below the configured sensitivity are ignored.
5. **Change Calculation:** The program calculates the percentage of pixels that changed.
6. **Alarm Activation:** If the percentage exceeds the configured threshold, Pygame activates the alarm.

## Limitations

- The system detects visual changes rather than identifying specific objects or people.
- Changes in applications, animations, or other screen elements can trigger the alarm.
- Detection sensitivity depends on the configured thresholds.
- The program currently monitors the primary display.

## Project Goals

This project explores real-time screen capture, image processing, change detection, and event-driven programming using Python.

It serves as a practical implementation of basic computer vision techniques and can be extended with more advanced detection methods in the future.

## Author

**proianis07**

GitHub: https://github.com/proianis07
