from image import PGMImage
import random
from gaussian import convolve

def apply_median_filter(image_pixels, filter_size):
    offset = filter_size // 2
    output = [[0] * len(row) for row in image_pixels]
    
    for i in range(offset, len(image_pixels) - offset):
        for j in range(offset, len(image_pixels[0]) - offset):
            values = []
            for x in range(-offset, offset + 1):
                for y in range(-offset, offset + 1):
                    values.append(image_pixels[i + x][j + y])
            output[i][j] = sorted(values)[len(values) // 2]
    
    return output

def salt_and_pepper_noise(image_pixels, percentage):
    output = [row[:] for row in image_pixels]
    num_changes = int(percentage * len(image_pixels) * len(image_pixels[0]) / 100)
    
    for _ in range(num_changes):
        i, j = random.randint(0, len(image_pixels) - 1), random.randint(0, len(image_pixels[0]) - 1)
        output[i][j] = 0 if random.random() < 0.5 else 255
        
    return output

def apply_averaging(image_pixels, filter_size):
    filter_vals = [[1/filter_size**2 for _ in range(filter_size)] for _ in range(filter_size)]
    return convolve(image_pixels, filter_vals) 

