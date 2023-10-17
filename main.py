from image import PGMImage
import numpy as np
import cv2
from correlation import correlate
from gaussian import apply_smoothing
from sharpening import unsharp_masking, high_boost_filtering
from median import apply_median_filter, salt_and_pepper_noise, apply_averaging

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

def get_user_choice():
    print("Which function do you want to test?")
    print("1. Correlation")
    print("2. Gaussian Smoothing with 7x7 mask")
    print("3. Gaussian Smoothing with 15x15 mask")
    print("4. Unsharp Masking")
    print("5. High-Boost Filtering")
    print("6. Salt and pepper noise")
    print("7. Median")
    print("8. Averaging")
    print("9. Sobel")

    choice = input("Enter the number of your choice: ")
    return choice

choice = get_user_choice()


if choice == "1":
    image = PGMImage()
    image.read_from_file('images\Image.pgm')
    small_image = PGMImage()
    small_image.read_from_file('images\Pattern.pgm')
    mask = small_image.pixels
    correlated_image = correlate(image, mask)
    new_file_name = 'correlated.pgm'
    correlated_image.write_to_file(new_file_name)
    print(f"New image written to {new_file_name}")

elif choice == "2":
    apply_smoothing('images/sf.pgm', '7x7')

elif choice == "3":
    apply_smoothing('images/sf.pgm', '15x15')

elif choice == "4":
    image = PGMImage()
    image.read_from_file('images/f_16.pgm')
    sharpened_pixels = unsharp_masking(image.pixels)
    sharpened_image = PGMImage(width=image.width, height=image.height, maxval=image.maxval)
    sharpened_image.pixels = sharpened_pixels
    sharpened_image.write_to_file('images/f_16_unsharp.pgm')

elif choice == "5":
    image = PGMImage()
    image.read_from_file('images/f_16.pgm')
    k = float(input("Enter the value for K: "))
    enhanced_pixels = high_boost_filtering(image.pixels, k)
    enhanced_image = PGMImage(width=image.width, height=image.height, maxval=image.maxval)
    enhanced_image.pixels = enhanced_pixels
    enhanced_image.write_to_file(f'images/f_16_high_boost_k{k}.pgm')

elif choice == "6":
    image = PGMImage()
    image.read_from_file('images/boat.pgm')
    noisy_image = salt_and_pepper_noise(image.pixels, 30)  # Adding 30% noise
    noisy_img_obj = PGMImage(width=image.width, height=image.height, maxval=image.maxval)
    noisy_img_obj.pixels = noisy_image
    noisy_img_obj.write_to_file('images/boat_noisy30.pgm')
    print("Noisy image generated!")

elif choice == "7":
    image = PGMImage()
    image.read_from_file('images/boat_noisy30.pgm')  # image already has noise
    filtered_image = apply_median_filter(image.pixels, 7)  # Using 7x7 filter
    filtered_img_obj = PGMImage(width=image.width, height=image.height, maxval=image.maxval)
    filtered_img_obj.pixels = filtered_image
    filtered_img_obj.write_to_file('images/boat30_7median.pgm')
    print("Median filtered image generated!")

elif choice == "8":
    
    image = PGMImage()
    image.read_from_file('images/boat_noisy30.pgm')  # image already has noise
    mask_size = input("Enter mask size (7 or 15): ")
    if mask_size == "7":
        mask_size = 7
        output_filename = 'images/boat_noisy30_averaged_7x7.pgm'
    elif mask_size == "15":
        mask_size = 15
        output_filename = 'images/boat_noisy30_averaged_15x15.pgm'
    else:
        print("Invalid choice.")
        exit()
    averaged_image = apply_averaging(image.pixels, mask_size)  
    averaged_img_obj = PGMImage(width=image.width, height=image.height, maxval=image.maxval)
    averaged_img_obj.pixels = averaged_image
    averaged_img_obj.write_to_file(output_filename)
    print("Averaged image generated!")

elif choice == "9":
    image = PGMImage()
    image.read_from_file('images\Lenna.pgm')
    maskx = [[-1,-2,-1],
            [0,0,0],
            [1,2,1]]
    masky = [[-1,0,1],
            [-2,0,2],
            [-1,0,1]]
    
    sobel_x = correlate(image, maskx)
    sobelx_file_name = 'sobel_x.pgm'

    sobel_y = correlate(image, masky)
    sobely_file_name = 'sobel_y.pgm'

    maginput = cv2.imread("images\Lenna.pgm")
    gray = cv2.cvtColor(maginput, cv2.COLOR_BGR2GRAY)
    gX = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
    gY = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
    magnitude = np.sqrt((gX ** 2) + (gY ** 2))
    magnitude = normalize_image(magnitude)
    magoutput = PGMImage()
    magoutput.read_from_file('images\Lenna.pgm')
    magoutput.pixels = magnitude
    magoutput.write_to_file("magnitude.pgm")

    sobel_x.write_to_file(sobelx_file_name)
    sobel_y.write_to_file(sobely_file_name)
    
    print(f"New image written to {sobelx_file_name}")
    print(f"New image written to {sobely_file_name}")

elif choice == "10":
    image = PGMImage()
    image.read_from_file('images\Lenna.pgm')
    prewittx = [[-1,-1,-1],
            [0,0,0],
            [1,1,1]]
    prewitty = [[-1,0,1],
            [-1,0,1],
            [-1,0,1]]
    
    prewitt_x = correlate(image, prewittx)
    prewittx_file_name = 'prewitt_x.pgm'

    prewitt_y = correlate(image, prewitty)
    prewitty_file_name = 'prewitt_y.pgm'

    maginput = cv2.imread("images\Lenna.pgm")
    gray = cv2.cvtColor(maginput, cv2.COLOR_BGR2GRAY)


    kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
    kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    img_prewittx = cv2.filter2D(maginput, -1, kernelx)
    img_prewitty = cv2.filter2D(maginput, -1, kernely)


    magnitude = np.sqrt((img_prewittx ** 2) + (img_prewitty ** 2))
    magnitude = normalize_image(magnitude)
    magoutput = PGMImage()
    magoutput.read_from_file('images\Lenna.pgm')
    magoutput.pixels = magnitude
    magoutput.write_to_file("magnitude_prewitt.pgm")

    prewitt_x.write_to_file(prewittx_file_name)
    prewitt_y.write_to_file(prewitty_file_name)
    print(f"New image written to {prewittx_file_name}")
    print(f"New image written to {prewitty_file_name}")

elif choice == "11":
    image = PGMImage()
    image.read_from_file('images\Lenna.pgm')
    mask = [[0,1,0],
            [1,-4,1],
            [0,1,0]]
    
    laplacian = correlate(image, mask)
    laplacian_file_name = 'laplacian.pgm'

    laplacian.write_to_file(laplacian_file_name)

    print(f"New image written to {laplacian_file_name}")

else:
    print("Invalid choice.")
    exit()

