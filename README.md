# EagleEye: Computer Vision Powered Automation 🦅 👁️

EagleEye is an automation utility designed to extract and verify digital booklets from web-based document viewers. It integrates browser orchestration with Optical Character Recognition (OCR) to address challenges in dynamic content capture and processing.

## Key Features
- **Computer Vision Pipeline:** Utilizes OpenCV for adaptive thresholding and image inversion to improve Tesseract OCR accuracy on complex UI elements.
- **State-Aware Navigation:** Monitors DOM changes and visual states to confirm page transitions, replacing static timer-based delays.
- **Fault Tolerance Logic:** Implements timeout-based recovery mechanisms to handle network interruptions or UI loading issues gracefully.
- **Data Verification:** Automatically cross-references captured data against expected numerical ranges to detect and report missing records.

## Tech Stack
- **Language:** Python 3.x
- **Automation:** Selenium WebDriver
- **OCR Engine:** Tesseract OCR
- **Image Processing:** OpenCV, NumPy, Pillow
- **Design Pattern:** Object-Oriented Programming (OOP)

## Project Structure
- `/assets`: Screenshots and UI flow diagrams.
- `/data`: Storage for captured booklets (ignored by git).
- `eagle_eye_pro.py`: The core engine.
- `requirements.txt`: List of dependencies.

## Installation
1. Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki).

