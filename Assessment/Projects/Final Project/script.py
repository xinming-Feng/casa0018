import time
import cv2
import numpy as np
import tensorflow as tf
import RPi.GPIO as GPIO
from picamera2 import Picamera2

def print_red(text):
    """Print text in red color (more noticeable)"""
    print(f"\033[91m{text}\033[0m")

# GPIO pin configuration (please modify according to actual wiring)
LED_RED = 17     # Red LED connected to GPIO 17
LED_GREEN = 27   # Green LED connected to GPIO 27

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(LED_GREEN, GPIO.OUT)
# Turn off all LEDs during initialization
GPIO.output(LED_RED, GPIO.LOW)
GPIO.output(LED_GREEN, GPIO.LOW)

# Initialize camera (configured for 224x224 capture, later preprocessed to 96x96)
picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (224, 224), "format": "RGB888"}
)
picam2.configure(config)
picam2.start()

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="./ei-window_final-classifier-tensorflow-lite-float32-model.3.lite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print_red(f"Input shape: {input_details[0]['shape']}")
print_red(f"Output shape: {output_details[0]['shape']}")

def preprocess(image):
    """
    Image preprocessing: Scale camera captured 224x224 image to 96x96,
    normalize to 0~1 range, and add batch dimension
    """
    # Use OpenCV to resize image
    image_resized = cv2.resize(image, (96, 96))  # Parameters order is (width, height)
    processed = image_resized / 255.0
    # Add batch dimension
    processed = np.expand_dims(processed, axis=0).astype(np.float32)
    return processed

try:
    frame_count = 0
    start_time = time.time()
    
    while True:
        # Capture image
        raw_image = picam2.capture_array()
        
        # Preprocess image
        input_data = preprocess(raw_image)
        
        # Perform inference
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        
        # Get model output
        raw_output = interpreter.get_tensor(output_details[0]['index'])
        # raw_output shape is typically [1, 2], index 0: probability of "OFF", index 1: probability of "ON"
        
        # Compare probabilities of both states, choose the higher one as recognition result
        if raw_output[0][1] > raw_output[0][0]:
            # Recognized as "ON": Turn on red LED, turn off green LED
            GPIO.output(LED_RED, GPIO.HIGH)
            GPIO.output(LED_GREEN, GPIO.LOW)
            result_str = "ON"
        else:
            # Recognized as "OFF": Turn on green LED, turn off red LED
            GPIO.output(LED_RED, GPIO.LOW)
            GPIO.output(LED_GREEN, GPIO.HIGH)
            result_str = "OFF"
        
        # Calculate frame rate and output information
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        frame_count += 1
        fps = frame_count / (time.time() - start_time)
        print_red(f"\n[{timestamp}] Frame rate: {fps:.2f}fps")
        print(f"Raw output: {raw_output}")
        print(f"Parsing result: Prediction is \"{result_str}\" [ OFF probability: {raw_output[0][0]:.4f}, ON probability: {raw_output[0][1]:.4f} ]")
        
        time.sleep(0.1)  # Control output frequency

except KeyboardInterrupt:
    picam2.stop()
    GPIO.output(LED_RED, GPIO.LOW)
    GPIO.output(LED_GREEN, GPIO.LOW)
    GPIO.cleanup()
    print_red("\nDetection stopped, camera and GPIO resources released")
