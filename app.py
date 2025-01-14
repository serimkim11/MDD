import serial
import time
from flask import Flask, render_template, request
import numpy as np
from tensorflow.keras.models import load_model

# Load model
model = load_model('apnea_detection_model.h5')

# Setup the Flask app
app = Flask(__name__)

# Setup serial communication (adjust the port and baud rate as per setup)
arduino = serial.Serial('/dev/ttyUSB0', 9600)  # Change to Arduino's port
time.sleep(2)  # Give time for the serial connection to establish

@app.route("/")
def index():
    return render_template("index.html")  # This loads the HTML form

@app.route("/predict", methods=["POST"])
def predict():
    # Check if the data is coming from the user input
    if request.form.get('heart_rate') and request.form.get('spo2') and request.form.get('breathing'):
        # Collect data from the form
        heart_rate = float(request.form['heart_rate'])
        spo2 = float(request.form['spo2'])
        breathing = float(request.form['breathing'])
    else:
        # Collect data from the Arduino
        if arduino.in_waiting > 0:
            data = arduino.readline().decode('utf-8').strip().split(',')
            heart_rate = float(data[0])
            spo2 = float(data[1])
            breathing = float(data[2])

    # Use the model to predict
    input_data = np.array([[heart_rate, spo2, breathing]])
    prediction = model.predict(input_data)
    result = "Sleep Apnea Detected" if prediction[0][0] > 0.5 else "Normal"
    
    # Return the result to the HTML page
    return render_template('index.html', prediction=result)

if __name__ == "__main__":
    app.run(debug=True)
