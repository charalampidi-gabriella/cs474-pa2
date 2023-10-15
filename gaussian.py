from image import PGMImage

gaussian_mask_7x7 = [
    [1, 1, 2, 2, 2, 1, 1],
    [1, 2, 2, 4, 2, 2, 1],
    [2, 2, 4, 8, 4, 2, 2],
    [2, 4, 8, 16, 8, 4, 2],
    [2, 2, 4, 8, 4, 2, 2],
    [1, 2, 2, 4, 2, 2, 1],
    [1, 1, 2, 2, 2, 1, 1]
]

gaussian_mask_15x15 = [
    [2, 3, 4, 5, 7, 8, 8, 8, 8, 8, 7, 5, 4, 3, 2],
    [3, 4, 6, 7, 9, 10, 11, 11, 11, 10, 9, 7, 6, 4, 3],
    [4, 6, 7, 9, 10, 12, 13, 13, 13, 12, 10, 9, 7, 6, 4],
    [5, 7, 9, 10, 12, 13, 14, 15, 14, 13, 12, 10, 9, 7, 5],
    [7, 9, 10, 12, 13, 14, 15, 16, 15, 14, 13, 12, 10, 9, 7],
    [8, 10, 12, 13, 14, 15, 16, 17, 17, 16, 15, 14, 13, 10, 8],
    [8, 11, 13, 14, 15, 16, 17, 19, 17, 16, 15, 14, 13, 11, 8],
    [8, 11, 13, 15, 16, 17, 18, 20, 18, 17, 16, 15, 13, 11, 8],
    [8, 10, 12, 13, 14, 15, 16, 17, 17, 16, 15, 14, 13, 10, 8],
    [7, 9, 10, 12, 13, 14, 15, 16, 15, 14, 13, 12, 10, 9, 7],
    [5, 7, 9, 10, 12, 13, 14, 15, 14, 13, 12, 10, 9, 7, 5],
    [4, 6, 7, 9, 10, 12, 13, 13, 13, 12, 10, 9, 7, 6, 4],
    [3, 4, 6, 7, 9, 10, 11, 11, 11, 10, 9, 7, 6, 4, 3],
    [2, 3, 4, 5, 7, 8, 8, 8, 8, 8, 7, 5, 4, 3, 2]
]

# Normalize 
total_value_15x15 = sum(sum(row) for row in gaussian_mask_15x15)
gaussian_mask_15x15 = [[val/total_value_15x15 for val in row] for row in gaussian_mask_15x15]


# Normalize the Gaussian mask
total = sum(sum(row) for row in gaussian_mask_7x7)
gaussian_mask_7x7 = [[val/total for val in row] for row in gaussian_mask_7x7]

def convolve(image, kernel):
    image_height = len(image)
    image_width = len(image[0])
    
    kernel_height = len(kernel)
    kernel_width = len(kernel[0])

    pad_height = kernel_height // 2
    pad_width = kernel_width // 2
    
    # Create a padded version of the image to handle boundaries
    padded_image = [[0] * (image_width + 2 * pad_width) for _ in range(image_height + 2 * pad_height)]
    for i in range(image_height):
        for j in range(image_width):
            padded_image[i + pad_height][j + pad_width] = image[i][j]
            
    output = [[0] * image_width for _ in range(image_height)]
    for i in range(image_height):
        for j in range(image_width):
            sum = 0
            for k in range(kernel_height):
                for l in range(kernel_width):
                    sum += kernel[k][l] * padded_image[i + k][j + l]
            output[i][j] = sum
            
    return output



def apply_smoothing(input_image_path, mask_size):
    image = PGMImage()
    image.read_from_file(input_image_path)
    if mask_size == "7x7":
        smoothed_image_pixels = convolve(image.pixels, gaussian_mask_7x7)
        output_filename = 'images/sf_smoothed_7x7.pgm'
    elif mask_size == "15x15":
        smoothed_image_pixels = convolve(image.pixels, gaussian_mask_15x15)
        output_filename = 'images/sf_smoothed_15x15.pgm'
    else:
        print("Invalid choice.")
        return

    smoothed_image = PGMImage(width=image.width, height=image.height, maxval=image.maxval)
    smoothed_image.pixels = smoothed_image_pixels
    smoothed_image.write_to_file(output_filename)