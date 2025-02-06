import cv2
import pytesseract
import os

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = '/bin/tesseract'  # Or the correct path

# Specify the folder containing the images
folder_path = "python/"

# Create or clear the output file before processing any images
with open("recognized.txt", "w") as file:
    file.write("")

# Loop through all files in the specified folder
for filename in os.listdir(folder_path):
    if filename.endswith((".jpg", ".png", ".jpeg")):  # Add other extensions if needed
        image_path = os.path.join(folder_path, filename)
        print(f"Processing: {image_path}") # Optional: Print which file is being processed

        try:
            img = cv2.imread(image_path)

            if img is None:  # Check if image was loaded correctly
                print(f"Error: Could not read image {image_path}")
                continue  # Skip to the next image

            # Preprocessing (same as before)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
            rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
            dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
            contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            im2 = img.copy()

            with open("recognized.txt", "a") as file:  # Open in append mode *inside* the loop
                for cnt in contours:
                    x, y, w, h = cv2.boundingRect(cnt)
                    #rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2) # Optional: draw rectangles, but slows things down
                    cropped = im2[y:y + h, x:x + w]
                    text = pytesseract.image_to_string(cropped)
                    file.write(text)
                    file.write("\n")

        except Exception as e:
            print(f"Error processing {image_path}: {e}")


print("Finished processing all images.")