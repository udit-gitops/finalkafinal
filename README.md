# Deepfake Detection System

A command-line deepfake detection system that can analyze images and videos to detect potential deepfakes using basic image processing techniques.

## Project Structure
```
deepfake_detection/
├── deepfake_detector.py   # Main detection script
├── requirements.txt       # Project dependencies
└── README.md             # This file
```

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Run the detection script:
```bash
python deepfake_detector.py
```

2. When prompted, enter the path to your image or video file.

## Features
- Support for images (JPG, PNG) and videos (MP4)
- Face detection and analysis
- Multiple detection metrics:
  - Edge density analysis
  - Color consistency check
  - Texture complexity analysis
- Detailed analysis report
- Confidence score calculation

## Usage
1. Run the script
2. Enter the path to your image or video file when prompted
3. View the analysis results, including:
   - Detection result (Deepfake/Authentic)
   - Confidence score
   - Detailed metrics for each detected face

## Note
This version uses basic image processing techniques and face detection to analyze potential deepfakes. While not as sophisticated as deep learning-based methods, it can detect common manipulation artifacts in images and videos. 