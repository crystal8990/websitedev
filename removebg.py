import cv2
import numpy as np
import os

# Define folder paths
input_folder = "removebg"
output_folder = "output"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

def remove_background(image_path, save_path):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define background color range (adjust as needed)
    lower_bound = np.array([0, 0, 180])  # Light backgrounds
    upper_bound = np.array([180, 40, 255])  # Adjust for mild shadows

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    background_removed = cv2.bitwise_and(image, image, mask=~mask)

    # Edge Detection (Refining the cutout)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    # Blend edges with background-removed image
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    final_result = cv2.addWeighted(background_removed, 0.8, edges_colored, 0.2, 0)

    cv2.imwrite(save_path, final_result)

# Process all images in the "removebg" folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):  # Process only images
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        remove_background(input_path, output_path)
        print(f"Processed: {filename}")

print("All images processed successfully! 🚀")
