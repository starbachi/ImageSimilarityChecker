from PIL import Image
import imagehash
import os
import glob
import subprocess
import time
import pygetwindow as gw
import pyautogui

# Ask for directory
directory = input("Please enter the directory: ")
similarity_threshold = int(input("Please enter the similarity threshold: "))

# Get all images, including those in subdirectories
image_files = glob.glob(os.path.join(directory, "**/*.[jp][np]g"), recursive=True)

# Calculate image hash
image_hashes = {image_file: imagehash.average_hash(Image.open(image_file)) for image_file in image_files}

# Convert the dictionary items to a list for easier indexing
image_list = list(image_hashes.items())

# Get screen size
screen_width, screen_height = pyautogui.size()

# Initialize counter for similarities
similarity_count = 0

# Compare each pair of images
for i in range(len(image_list)):
    image_file1, hash1 = image_list[i]
    for j in range(i+1, len(image_list)):
        image_file2, hash2 = image_list[j]
        if hash1 - hash2 < similarity_threshold:
            # Check if the files still exist
            if not os.path.exists(image_file1):
                image_hashes.pop(image_file1)
                continue
            if not os.path.exists(image_file2):
                image_hashes.pop(image_file2)
                continue

            print(f"{os.path.basename(image_file1)} is similar to {os.path.basename(image_file2)}")
            similarity_count += 1  # Increment the counter
            input("Press Enter to open the images...")
            subprocess.run(["explorer", image_file1], shell=True)
            subprocess.run(["explorer", image_file2], shell=True)
            time.sleep(1)  # Wait for the windows to open

            # Get the windows
            windows = gw.getWindowsWithTitle('Photos')

            # Move the windows
            for k, window in enumerate(windows):
                window.moveTo(k * screen_width // 2, 0)
                window.resizeTo(screen_width // 2, screen_height)

# Check if no similarities were found
if similarity_count == 0:
    print("No similarities were found.")
    input("Press Enter to close the command prompt...")

# If similarities were found, print the count
else:
    print(f"Found {similarity_count} similarities.")