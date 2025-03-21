# Stopwatch Number Detection

This project is an application for detecting and recognizing digits on stopwatches within a video stream from a camera, utilizing the YOLO (You Only Look Once) model. The application can detect up to two stopwatches in a single frame, recognize the displayed digits, and save both the images and detected times into a CSV file.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Description
The "Stopwatch Number Detection" project is designed to detect and recognize digits on stopwatches appearing in a video stream from a camera. Leveraging two YOLO models—one for detecting stopwatch boxes and another for recognizing digits—this application can:
- Detect up to two stopwatches in a single video frame.
- Recognize digits (0-9, `-`, `.`, `D`) displayed on the stopwatches.
- Save detected stopwatch images to the `./frames/` directory.
- Record the detected times into a CSV file at `./result/result.csv`.

## Features
- **Stopwatch Detection**: Identifies stopwatch boxes in video frames and marks them with green rectangles labeled "1" or "2".
- **Digit Detection**: Recognizes digits (0-9, `-`, `.`, `D`) on stopwatches and converts them into a formatted time string.
- **Automatic Saving**: Saves images and detected times to a CSV file when the digits remain unchanged for 3 consecutive frames.
- **Detection Reset**: Resets the detection process if a stopwatch displays all '0' digits.
- **Camera Selection**: Allows users to choose from available cameras for video streaming.

## Installation
To run this project, you’ll need a Python environment with the required dependencies. Follow the steps below to install and set up the application.

### Prerequisites
- Python 3.7 or higher
- OpenCV (`opencv-python`)
- Ultralytics YOLO (`ultralytics`)
- CSV (built-in Python module)
- An operating system with camera access

### Installation Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/IvanSholana/StopWatch-Project.git
   cd stopwatch-number-detection
   ```

2. **Install Dependencies**
   Create a `requirements.txt` file with the following content:
   ```
   opencv-python
   ultralytics
   ```
   Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download YOLO Models**
   Ensure the required YOLO models are available in the `./model/` directory:
   - `best.pt`: Model for digit detection.
   - `kotak_stopwatch.pt`: Model for stopwatch box detection.
   If you don’t have these models, you’ll need to train them yourself using an appropriate dataset or download pre-trained models.

4. **Run the Application**
   ```bash
   python main.py
   ```

## Usage
After running the application with `python main.py`, you’ll be prompted to select an available camera. Once a camera is chosen, the application will begin capturing the video stream and detecting stopwatches and their digits.

- **Stopwatch Detection**: Green rectangles will appear around detected stopwatches, labeled "1" or "2".
- **Digit Detection**: Detected digits on the stopwatch will be processed and formatted into a time string (e.g., `1:23:45:678`).
- **Saving**: If the digits on a stopwatch remain unchanged for 3 consecutive frames, the stopwatch image will be saved to `./frames/` with filenames like `1.jpg`, `2.jpg`, etc., and the detected time will be logged in `./result/result.csv`.
- **Stopping the Application**: Press the `q` key in the video window to exit the application.

### Example CSV Output
The `./result/result.csv` file will contain data in the following format:
```
1,1:23:45:678,Stopwatch 1,1
2,0:12:34:567,Stopwatch 2,2
```

## Project Structure
Here’s the directory structure of the project:
```
stopwatch-number-detection/
│
├── frames/                 # Directory for storing detected images
├── model/                  # Directory for YOLO models
│   ├── best.pt             # YOLO model for digit detection
│   └── kotak_stopwatch.pt  # YOLO model for stopwatch box detection
├── result/                 # Directory for CSV result file
│   └── result.csv          # CSV file logging detected times and image filenames
├── main.py                 # Main script to run the application
├── requirements.txt        # List of Python dependencies
└── README.md               # This README file
```

## Contributing
We warmly welcome contributions to this project. To contribute, please follow these steps:
1. Fork this repository.
2. Create a new branch for your feature or fix (`git checkout -b new-feature`).
3. Commit your changes (`git commit -m "Added new feature"`).
4. Push to your branch (`git push origin new-feature`).
5. Create a Pull Request on GitHub.

Please describe your changes and the reasoning behind them in the Pull Request.
