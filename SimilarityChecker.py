from PIL import Image
import imagehash
import os
import glob

# Ask for directory
directory = input("Please enter the directory: ")
similarity_threshold = int(input("Please enter the similarity threshold: "))

# Get all images
image_files = glob.glob(os.path.join(directory, "*.[jp][np]g"))

# Calculate image hash
image_hashes = {image_file: imagehash.average_hash(Image.open(image_file)) for image_file in image_files}

# Don't present reported pairs
reported_pairs = set()

# Compare each pair of images
for image_file1, hash1 in image_hashes.items():
    for image_file2, hash2 in image_hashes.items():
        if image_file1 != image_file2 and hash1 - hash2 < similarity_threshold:
            # Sort pair for easier comparison
            pair = tuple(sorted((image_file1, image_file2)))
            if pair not in reported_pairs:
                print(f"{os.path.basename(image_file1)} is similar to {os.path.basename(image_file2)}")
                reported_pairs.add(pair)