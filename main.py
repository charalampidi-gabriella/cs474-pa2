from image import PGMImage
from correlation import correlate
from gaussian import apply_smoothing
from sharpening import unsharp_masking, high_boost_filtering

def get_user_choice():
    print("Which function do you want to test?")
    print("1. Correlation")
    print("2. Gaussian Smoothing with 7x7 mask")
    print("3. Gaussian Smoothing with 15x15 mask")
    print("4. Unsharp Masking")
    print("5. High-Boost Filtering")

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
    apply_smoothing('images/lenna.pgm', '7x7')

elif choice == "3":
    apply_smoothing('images/lenna.pgm', '15x15')

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

else:
    print("Invalid choice.")
    exit()
