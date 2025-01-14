import serial
import time
import numpy as np
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model('apnea_detection_model.h5')

# Setup the Flask app
app = Flask(__name__)

# Configure the Bluetooth connection
bluetooth = serial.Serial('/dev/tty.HC-05', 9600)  # Replace 'COM6' with the port your HC-05/06 is connected to
time.sleep(2)  # Wait for the connection to establish

@app.route("/")
def index():
    return render_template("index.html")  # Load the HTML page

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Read data from Bluetooth
        if bluetooth.in_waiting > 0:
            data = bluetooth.readline().decode('utf-8').strip().split(',')
            heart_rate = float(data[0])
            spo2 = float(data[1])
            breathing = float(data[2])

            # Prepare the data for prediction
            input_data = np.array([[heart_rate, spo2, breathing]])
            prediction = model.predict(input_data)
            result = "Sleep Apnea Detected" if prediction[0][0] > 0.5 else "Normal"
        else:
            result = "No data received from Bluetooth."
    except Exception as e:
        result = f"Error: {e}"

    # Return the result to the HTML page
    return render_template('index.html', prediction=result)

if __name__ == "__main__":
    app.run(debug=True)
