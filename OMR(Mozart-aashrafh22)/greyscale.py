from skimage import io, color
import os
import numpy as np

def to_grayscale(img):
    if img.shape[-1] == 4:
        # Convert RGBA to RGB
        img = color.rgba2rgb(img)
    # Convert RGB to Grayscale
    gray = color.rgb2gray(img)
    return gray

def main():
    input_directory = r'C:\Sheet\greyin'
    output_directory = r'C:\Sheet\greyout'

    # Check if output directory exists, if not, create it
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Process all PNG images in the input directory
    for filename in os.listdir(input_directory):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(input_directory, filename)
            output_filename = f"{os.path.splitext(filename)[0]}_grayscale.png"
            output_path = os.path.join(output_directory, output_filename)

            # Read the image from the input directory
            image = io.imread(input_path)

            # Convert the image to grayscale
            grayscale_image = to_grayscale(image)

            # Convert the grayscale image to 8-bit unsigned integers
            grayscale_image = (grayscale_image * 255).astype(np.uint8)

            # Save the grayscale image to the output directory
            io.imsave(output_path, grayscale_image)
            print(f"Processed {filename} to grayscale.")

if __name__ == "__main__":
    main()
