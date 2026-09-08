import time
import joblib
import pandas as pd
import os

print("--- Initializing Real-Time Exoskeleton Control Loop ---")

# 1. Load the trained model and test stream exported from your Jupyter Notebook
# Adjust relative paths if your folders are structured differently
model_path = '../notebooks/emg_random_forest_model.pkl'  # Update path if needed
data_path = '../notebooks/sample_test_stream.pkl'      # Update path if needed

if not os.path.exists(model_path):
    # Fallback to current directory if files were copied locally
    model_path = 'emg_random_forest_model.pkl'
    data_path = 'sample_test_stream.pkl'

model = joblib.load(model_path)
X_test_stream = pd.read_pickle(data_path)

print("Trained model and test stream loaded successfully!")

def exoskeleton_controller(prediction):
    if prediction == 'leg up':
        return "ACTUATOR COMMAND: Apply upward torque to hip and knee motors."
    elif prediction == 'leg down':
        return "ACTUATOR COMMAND: Engage controlled braking/dampening for smooth descent."
    elif prediction == 'leg move':
        return "ACTUATOR COMMAND: Maintain swing-phase trajectory assistance."
    else:
        return "ACTUATOR COMMAND: Hold current rigid position (Idle/Stand)."

for i in range(len(X_test_stream)):
    # Capture live 200ms window features
    live_features = X_test_stream.iloc[[i]]
    
    # ML Model predicts user intent using your actual trained notebook model
    predicted_movement = model.predict(live_features)[0]
    
    # State machine determines mechanical assistance
    motor_action = exoskeleton_controller(predicted_movement)
    
    print(f"[{i * 200}ms Latency Window] Intent: {predicted_movement.upper()} --> {motor_action}")
    
    # Simulate hardware processing delay (200ms window step)
    time.sleep(0.2)

print("\n--- Exoskeleton Simulation Complete Using Notebook Model! ---")