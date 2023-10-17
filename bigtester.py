import numpy as np
import sys

def load_pgm_image(filename):
        with open(filename, 'rb') as f:
            # Read header
            header = f.readline().decode().strip()
            if header != 'P5':
                raise ValueError('Not a PGM file')
            # Skip comments
            while True:
                line = f.readline().strip()
                if line and not line.startswith(b'#'):
                    break
            width, height = map(int, line.split())
            maxval = int(f.readline().strip())
            # Read data
            pixels = [
                [int.from_bytes(f.read(1), 'big') for _ in range(width)]
                for _ in range(height)
            ]
            return width,height,maxval,pixels

def save_pgm_image(file_path, image_data, width, height, max_pixel_value):
    with open(file_path, 'w') as f:
        f.write("P2\n")
        f.write(f"{width} {height}\n")
        f.write(f"{max_pixel_value}\n")
        f.write(" ".join(map(str, image_data.tolist())))

def correlate_images(image, kernel):
    # Get image dimensions
    image_height, image_width = image.shape
    kernel_height, kernel_width = kernel.shape

    # Calculate padding size for the image
    pad_height = kernel_height // 2
    pad_width = kernel_width // 2

    # Create a zero-padded image
    padded_image = np.pad(image, ((pad_height, pad_height), (pad_width, pad_width)), mode='constant')

    # Initialize an empty result image
    result_image = np.zeros_like(image)

    # Perform 2D correlation
    for i in range(image_height):
        for j in range(image_width):
            result_image[i, j] = np.sum(padded_image[i:i+kernel_height, j:j+kernel_width] * kernel)

    return result_image

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: python image_correlation.py input_image.pgm kernel_image.pgm output_image.pgm")

    input_image_path = sys.argv[1]
    kernel_image_path = sys.argv[2]
    output_image_path = sys.argv[3]

    # Load input image and kernel
    input_image_data, input_image_width, input_image_height, _ = load_pgm_image(input_image_path)
    kernel_image_data, kernel_width, kernel_height, _ = load_pgm_image(kernel_image_path)

    # Check if kernel size is odd
    if kernel_width % 2 == 0 or kernel_height % 2 == 0:
        sys.exit("Kernel size must be odd.")

    # Perform correlation
    # result_image = correlate_images(np.reshape(input_image_data,(input_image_height, input_image_width)), np.reshape(kernel_image_data,(kernel_height, kernel_width)))
    result_image = correlate_images(input_image_data,kernel_image_data,)

    # Save the result as a PGM image
    save_pgm_image(output_image_path, result_image, input_image_width, input_image_height, 255)

    print(f"Correlation result saved to {output_image_path}")