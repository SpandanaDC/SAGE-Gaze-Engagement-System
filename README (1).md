# 👁️ SAGE: Saccade-Aware Gaze Engagement System

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Face%25Mesh-orange.svg)](https://developers.google.com/mediapipe)
[![Platform](https://img.shields.io/badge/Edge%20Target-Raspberry%20Pi-red.svg)](https://www.raspberrypi.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**An Edge-AI Powered Assistive Gaze-Tracking, AAC Communication, and Real-Time Clinical Telemetry Suite for Motor-Impaired Patients.**

</div>

---

## 🚀 Executive Summary

Commercial assistive eye-tracking and AAC (Augmentative and Alternative Communication) hardware solutions are cost-prohibitive for widespread clinical and home-care adoption. **SAGE** bridges this gap by transforming standard RGB webcams into high-precision, low-latency gaze trackers running on local edge hardware (Raspberry Pi). 

Beyond accessibility, SAGE introduces an autonomous **clinical telemetry bridge** that tracks patient fatigue states in real-time and dispatches high-priority alerts directly to nursing stations.

---

## 🛠️ Core System Architecture

SAGE is built on a modular, multi-threaded **Edge-to-Station Architecture**:
graph TD
    Webcam["Standard RGB Webcam"] --> Landmarks["MediaPipe 478 3D Landmarks"]
    
    Landmarks --> EAR["EAR Fatigue Analyzer"]
    EAR --> Bridge["Shared File Bridge"]
    
    Landmarks --> ML["Supervised ML Regressor"]
    ML --> Kalman["Kalman Filter Smoothing"]
    Kalman --> Dashboard["Nurse Telemetry Dashboard"]
    Bridge --> Dashboard
    
    ML --> AAC["AAC Grid & Async TTS Engine"]
---

## ✨ Key Features

* **Non-Invasive Computer Vision Pipeline:** Extracts 478 3D facial landmarks via Google MediaPipe at 30 FPS using standard webcams, eliminating the need for expensive infrared hardware.
* **Supervised Machine Learning Model Selection:** Dynamically trains and evaluates multiple regression models (**Ridge Regression, Random Forest, MLP, and HistGradientBoosting**) during a 66-point calibration routine to select the lowest-error mapping function.
* **Kalman Filtering & Noise Rejection:** Implements time-aware velocity capping and confidence-gated Kalman filtering to eliminate cursor jitter caused by micro-saccades or sub-pixel camera noise.
* **Asynchronous Text-to-Speech (TTS):** Features a non-blocking background worker process that dispatches instant audio output without freezing the patient interface grid.
* **Automated Clinical Fatigue Triage:** Calculates Eye Aspect Ratio (EAR) with a 1.5-second temporal debounce threshold to distinguish natural blinks from pathological fatigue, automatically logging high-priority medical requests for nursing staff.

---

## 🧰 Technology Stack

| Component | Technology Used | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.9+ | Core application logic, computer vision, and machine learning pipeline. |
| **Computer Vision** | OpenCV (`cv2`), MediaPipe | Real-time video capture, facial landmark extraction, and head-pose estimation (`solvePnP`). |
| **Machine Learning** | Scikit-Learn | Supervised regression training and coordinate mapping. |
| **User Interface** | Tkinter | Lightweight, responsive Patient AAC communication grid and Nurse Dashboard. |
| **Audio Engine** | `pyttsx3` | Offline, multi-threaded text-to-speech synthesis. |
| **Target Edge Hardware** | Raspberry Pi (ARM Cortex) | Low-power, privacy-first bedside deployment node. |

---

## 📂 Project Structure

```text
eye_controlled_mouse/
│
├── aac_board.py          # Patient communication grid & async TTS dispatcher
├── eye_gaze.py           # Supervised regression calibration & main runtime loop
├── gaze_lib.py           # Feature extraction, EAR math, & Kalman filter module
├── fatigue_status.txt    # Inter-process telemetry bridge data log
└── README.md             # Project documentation
