from PIL import Image
import os

# Folder containing your car images
image_folder = "static/images/"

# Desired size
width, height = 800, 600  # you can change this

# Loop through all files in the folder
for filename in os.listdir(image_folder):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        img_path = os.path.join(image_folder, filename)
        with Image.open(img_path) as img:
            # Resize image
            img = img.resize((width, height))
            # Save the resized image back
            img.save(img_path)
            print(f"Resized {filename} to {width}x{height}")
