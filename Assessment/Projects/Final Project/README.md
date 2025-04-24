# Final Project



### Definition of problem being solved 
This project aims to build a camera-based deep learning system that detects whether a window is open or closed. Motivated by real-life issues like noise and weather intrusion due to forgotten open windows, the system uses a CNN model to process image data and triggers LED indicators for real-time feedback.

 - Data: 228 original images (RGB, various angles and lighting), expanded to 534 via data augmentation.

 - Goal: Real-time, accurate window state detection using low-cost hardware (Raspberry Pi + Camera Module 3).

### Documentation of experiments and results 
 - Model: CNN chosen for its performance in image recognition; refined by adjusting convolution layers and adding dense layers after dropout.

 - Best Architecture:
   
Input → Conv2D + Pool → Flatten → Dropout → Dense → Output
Achieved 71.56% accuracy on test data.

 - Comparisons:

1. CNN outperformed MobileNetV1 (≈50% accuracy).

2.RGB images yielded better results than grayscale.

 - Deployment: Model converted to TensorFlow Lite, runs on Raspberry Pi, controls red/green LEDs based on predicted probabilities.

### Critical reflection and learning from experiments 


 - Challenges:

1. Accuracy dropped with camera movement or visual obstructions.

2. Poor performance on mesh-covered or curtain-blocked windows.

 - Next Steps:

1. Collect more diverse data (e.g. windows with mesh/screens).

2. Explore depth-based features for improved transparency handling.

3. Enhance hardware with LCD display or sound alerts.

Overall, the project shows strong potential for practical smart home use, with room for improvement in data and feature design.

# files meaning

