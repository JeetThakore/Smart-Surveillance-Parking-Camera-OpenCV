# Smart-Surveillance-Parking-Camera-OpenCV

YouTube Video Link (Live Project Demo and Faculty Feedback): https://www.youtube.com/watch?v=rS8tCiAn4aM

# Smart Surveillance Parking Camera

## Overview

This project, led by Dr. Raghavendra Bhalerao, developed a Smart Surveillance Parking Camera system aimed at conserving energy in underground parking lots. The primary objective was to reduce overall energy consumption by selectively activating lights only when a vehicle is detected underneath.

## Features

- Utilizes computer vision technology to track vehicle movement and activate corresponding lights.
- Implements image processing algorithms using OpenCV for accurate detection.
- Proposes future enhancements, including integration with a stand-alone microcontroller for increased portability.
- Demonstrates a working prototype using Arduino and PyFirmata.

## How It Works

1. **Video Processing:** The system processes video footage from a camera using OpenCV to track vehicle movement.
2. **Energy Conservation:** Lights are selectively activated based on detected vehicles, reducing unnecessary energy wastage.
3. **Arduino Integration:** The system is integrated with Arduino and PyFirmata to control the activation of lights.

## Code Structure

The project includes Python code (`Smart_Surveillance_Parking_Camera.py`) for video processing and energy conservation. Additionally, an Arduino script (`Arduino_Code.ino`) demonstrates the integration with hardware components.

## Dependencies

- OpenCV
- NumPy
- Matplotlib
- screen_brightness_control
- PyFirmata

## Usage

1. Clone the repository.
2. Run the Python script `Smart_Surveillance_Parking_Camera.py` for video processing.
3. Upload the Arduino script `Arduino_Code.ino` to your Arduino board.
4. Connect the hardware components as per the provided guidelines.

## Contribution

Contributions to enhance the system's functionality or improve code efficiency are welcome. Feel free to open issues or pull requests.

## Future Enhancements

The project suggests future enhancements, including integrating the system with a stand-alone microcontroller for increased portability and wider applicability in various settings.

## Acknowledgments

- Dr. Raghavendra Bhalerao
- Jeet Pranav
- Satyajeet K Verma (2022)

