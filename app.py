import serial
import time
import numpy as np
from flask import Flask, render_template
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model('apnea_detection_model.h5')

# Setup the Flask app
app = Flask(__name__)

# Configure the Bluetooth connection
bluetooth = serial.Serial('/dev/tty.HC-05', 9600)  
time.sleep(2)  # Wait for the connection to establish

@app.route("/")
def index():
    try:
        # Read data from Bluetooth
        if bluetooth.in_waiting > 0:
            # Read a line of data from the Bluetooth module
            data = bluetooth.readline().decode('utf-8').strip().split(',')
            
            # Parse the heart rate value
            heart_rate = float(data[0])
            
            # Placeholder values for spo2 and breathing
            spo2 = 98.0  # Normal SpO2 value
            breathing = 15.0  # Normal breathing rate
            
            # Prepare the data for prediction
            input_data = np.array([[heart_rate, spo2, breathing]])
            prediction = model.predict(input_data)

            # Interpret the result
            result = "Sleep Apnea Detected" if prediction[0][0] > 0.5 else "Normal"
        else:
            result = "Waiting for data from Arduino..."
    except Exception as e:
        result = f"Error: {e}"

    # Render the result on the webpage
    return render_template("index.html", prediction=result)

if __name__ == "__main__":
    app.run(debug=True)
