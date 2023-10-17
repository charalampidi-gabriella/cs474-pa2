##############################CORRECT
import numpy as np

from image import PGMImage
def normalize_image(image_pixels):
    min_val = min(map(min, image_pixels))
    max_val = max(map(max, image_pixels))

    height = len(image_pixels)
    width = len(image_pixels[0])
    
    normalized_pixels = [[0] * width for _ in range(height)]
    
    for r in range(height):
        for c in range(width):
            normalized_pixels[r][c] = int(255*(image_pixels[r][c] - min_val) / (max_val - min_val))
    
    return normalized_pixels


def correlate(image, mask):
    mask_height = len(mask)
    mask_width = len(mask[0])

    if mask_height % 2 == 0 or mask_width % 2 == 0:
        raise ValueError("Mask dimensions should be odd")

    h = mask_height // 2
    w = mask_width // 2

    correlated_image = PGMImage(image.width, image.height, image.maxval)

    print("Starting correlation...")

    for r in range(image.height):
        if r % 10 == 0:  # Print every 10 rows to reduce the number of print statements
            print(f"Processing row {r}")

        for c in range(image.width):
            sum = 0

            for u in range(-h, h + 1):
                for v in range(-w, w + 1):
                    rr = r + u
                    cc = c + v

                    # If outside the boundary of the image, treat pixel value as 0
                    if 0 <= rr < image.height and 0 <= cc < image.width:
                        pixel_val = image.pixels[rr][cc]
                    else:
                        pixel_val = 0

                    sum += mask[u + h][v + w] * pixel_val

            correlated_image.pixels[r][c] = sum

    print("Normalization starting...")
    normalized_pixels = normalize_image(correlated_image.pixels)
    correlated_image.pixels = normalized_pixels
    print("Normalization completed.")

    return correlated_image
