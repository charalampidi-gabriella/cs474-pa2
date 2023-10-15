from image import PGMImage
from correlation import correlate
from gaussian import apply_smoothing
from sharpening import unsharp_masking, high_boost_filtering
from median import apply_median_filter, salt_and_pepper_noise, apply_averaging


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

    choice = input("Enter the number of your choice: ")
    return choice

choice = get_user_choice()
image = PGMImage()
image.read_from_file('images/lenna.pgm')

if choice == "1":
    small_image = PGMImage()
    small_image.read_from_file('images/Pattern.pgm')
    mask = small_image.pixels
    correlated_image = correlate(image, mask)
    new_file_name = 'images/correlated.pgm'
    correlated_image.write_to_file(new_file_name)
    print(f"New image written to {new_file_name}")

elif choice == "2":
    apply_smoothing('images/sf.pgm', '7x7')

elif choice == "3":
    apply_smoothing('images/sf.pgm', '15x15')

elif choice == "4":
    sharpened_pixels = unsharp_masking(image.pixels)
    sharpened_image = PGMImage(width=image.width, height=image.height, maxval=image.maxval)
    sharpened_image.pixels = sharpened_pixels
    sharpened_image.write_to_file('images/lenna_unsharp.pgm')

elif choice == "5":
    k = float(input("Enter the value for K: "))
    enhanced_pixels = high_boost_filtering(image.pixels, k)
    enhanced_image = PGMImage(width=image.width, height=image.height, maxval=image.maxval)
    enhanced_image.pixels = enhanced_pixels
    enhanced_image.write_to_file(f'images/lenna_high_boost_k{k}.pgm')

elif choice == "6":
    image = PGMImage()
    image.read_from_file('images/lenna.pgm')
    noisy_image = salt_and_pepper_noise(image.pixels, 30)  # Adding 30% noise
    noisy_img_obj = PGMImage(width=image.width, height=image.height, maxval=image.maxval)
    noisy_img_obj.pixels = noisy_image
    noisy_img_obj.write_to_file('images/lenna_noisy.pgm')
    print("Noisy image generated!")

elif choice == "7":
    image = PGMImage()
    image.read_from_file('images/lenna_noisy.pgm')  # image already has noise
    filtered_image = apply_median_filter(image.pixels, 7)  # Using 7x7 filter
    filtered_img_obj = PGMImage(width=image.width, height=image.height, maxval=image.maxval)
    filtered_img_obj.pixels = filtered_image
    filtered_img_obj.write_to_file('images/lenna_filtered.pgm')
    print("Median filtered image generated!")

elif choice == "8":
    
    image = PGMImage()
    image.read_from_file('images/sf.pgm')  # image already has noise
    mask_size = input("Enter mask size (7 or 15): ")
    if mask_size == "7":
        mask_size = 7
        output_filename = 'images/sf_averaged_7x7.pgm'
    elif mask_size == "15":
        mask_size = 15
        output_filename = 'images/sf_averaged_15x15.pgm'
    else:
        print("Invalid choice.")
        exit()
    averaged_image = apply_averaging(image.pixels, mask_size)  
    averaged_img_obj = PGMImage(width=image.width, height=image.height, maxval=image.maxval)
    averaged_img_obj.pixels = averaged_image
    averaged_img_obj.write_to_file(output_filename)
    print("Averaged image generated!")

else:
    print("Invalid choice.")
    exit()

