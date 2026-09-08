# EMG-Based Lower-Limb Movement Classification

## Project Overview
This repository contains an end-to-end machine learning pipeline that classifies lower-limb physical movements using single-channel surface electromyography (EMG) signals. The system is designed to decode muscular intent in real-time, acting as a foundational prototype for controlling lower-limb assistive devices like prostheses or robotic exoskeletons.

## Dataset
This project utilizes the **"Electromyography Signal Dataset for Controlling Lower Limb Prostheses"** sourced from Mendeley Data. The dataset provides continuous, labeled recordings categorized into three distinct movement classes:
* **Leg Up** 
* **Leg Down** 
* **Leg Move**

## Machine Learning Pipeline
### 1. Signal Preprocessing
Raw surface EMG signals are inherently corrupted by environmental and motion-related noise. The data is cleaned using a 4-step biological signal processing pipeline via SciPy:
* **Bandpass Filtering:** A 20Hz - 450Hz Butterworth filter attenuates low-frequency motion artifacts and high-frequency noise.
* **Notch Filtering:** A 50Hz notch filter eliminates alternating current (AC) power-line interference.
* **Rectification:** Full-wave rectification maps negative electrical spikes into positive magnitudes to reflect total contraction power.
* **Smoothing:** A 10Hz low-pass filter creates a clean "linear envelope" matching the physical contraction shape of the muscle.

### 2. Feature Extraction
To prepare the time-series data for standard classification algorithms, the signals are converted into a tabular dataset.
* **Windowing:** Signals are segmented into 200-millisecond sliding windows with a 100-millisecond (50%) overlap to keep processing latency within human motor limits.
* **Time-Domain Features:** Four statistical features are extracted per window: Mean Absolute Value (MAV), Root Mean Square (RMS), Variance, and Waveform Length (WL).

### 3. Model Training & Validation
* **Model:** A **Random Forest Classifier** was selected for its ability to model non-linear relationships across time-domain features and its robustness against biological outliers.
* **Evaluation:** To prevent temporal data leakage caused by the 50% overlap in sliding windows, a **5-fold GroupKFold cross-validation** scheme was implemented, ensuring the model was tested strictly on unseen continuous movement blocks.
* **Results:** The system achieved a Mean GroupKFold Accuracy of **90.32% **. 
* **Limitations:** Due to severe class imbalance, the system struggles with the minority "Leg Up" class (0.37 recall), identifying a critical area for future algorithmic balancing or synthetic data generation (SMOTE).

## Exoskeleton Integration (Bonus Task)
The project includes a simulated state machine controller demonstrating how the ML model triggers real-time physical assistance. Based on the Random Forest predictions, the system maps output to specific motor commands:
* **Leg Up:** Applies upward torque to hip and knee motors.
* **Leg Down:** Applies controlled braking/dampening for smooth descent.
* **Leg Move:** Engages swing-phase motor assistance.

## Repository Structure
```text
emg-lower-limb-classification/
│
├── dataset/                   # Contains the Mendeley dataset 
├── notebooks/              # Core workspace[cite: 1]
│   └── EMG_Classification.ipynb [cite: 1]
|
├── .gitignore              # Ignores large data files and system files[cite: 1]
├── requirements.txt        # List of dependencies[cite: 1]
└── README.md               # Project documentation[cite: 1]