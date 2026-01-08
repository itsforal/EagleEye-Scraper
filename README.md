# EagleEye: Computer Vision Powered Automation 🦅

EagleEye is a robust, production-grade automation tool designed to extract and verify digital booklets from web-based document viewers. It combines browser orchestration with Optical Character Recognition (OCR) to solve the "Dynamic Content Capture" problem.

## 🚀 Key Features
- **Computer Vision Pipeline**: Uses OpenCV for adaptive thresholding and image inversion to maximize Tesseract OCR accuracy on complex UI sidebars.
- **State-Aware Automation**: Instead of simple timers, the bot monitors the DOM and visual state to confirm page transitions.
- **Resilience Engineering**: Implements a timeout-based recovery system to bypass stuck network requests or UI glitches.
- **Integrity Reporting**: Automatically cross-references captured data against expected numerical ranges to identify missing records.

## 🛠 Tech Stack
- **Language**: Python 3.x
- **Automation**: Selenium WebDriver
- **OCR Engine**: Tesseract OCR
- **Image Processing**: OpenCV, NumPy, Pillow
- **Design Pattern**: Object-Oriented Programming (OOP)

## 📦 Project Structure
- `/assets`: Screenshots and UI flow diagrams.
- `/data`: Storage for captured booklets (ignored by git).
- `eagle_eye_pro.py`: The core engine.
- `requirements.txt`: List of dependencies.

## ⚙️ Installation
1. Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki).
2. Clone this repository:
   ```bash
   git clone https://github.com/your-username/eagle-eye.git