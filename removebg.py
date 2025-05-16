
import cv2
import numpy as np
import os
from PIL import Image

# Define folder paths
input_folder = "removebg"
output_folder_transparent = "output_transparent"

# Ensure output folder exists
os.makedirs(output_folder_transparent, exist_ok=True)

def remove_background(image_path, transparent_save_path):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define background color range (adjust as needed)
    lower_bound = np.array([0, 0, 180])  # Light backgrounds
    upper_bound = np.array([180, 40, 255])  # Adjust for mild shadows

    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # **Apply Gaussian blur** for smooth edge transitions
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    # Convert to RGBA for transparency
    image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    image_rgba[:, :, 3] = cv2.bitwise_not(mask)  # Alpha channel based on mask

    # Convert to WebP with transparency using Pillow
    final_result_pil = Image.fromarray(cv2.cvtColor(image_rgba, cv2.COLOR_BGRA2RGBA))
    webp_transparent_path = transparent_save_path.replace(".jpg", ".webp").replace(".png", ".webp")
    final_result_pil.save(webp_transparent_path, "WEBP", quality=90)

    print(f"Processed: {os.path.basename(image_path)}")
    print(f"Saved Transparent WebP: {webp_transparent_path}")

# Process all images in the "removebg" folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        input_path = os.path.join(input_folder, filename)
        transparent_output_path = os.path.join(output_folder_transparent, filename)
        remove_background(input_path, transparent_output_path)

print("All images processed with Gaussian blur & transparent background removal! 🚀")


# FULLY WORKS FOR WHITE BACKGROUNDS AND CONTRASTING COLORS ON A WHITE BACKGROUND BUT NEEDS IMPROVEMENT FOR WHITE OBJECTS ON A BLACK BACKGROUND
