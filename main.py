from image import PGMImage
from correlation import correlate
from gaussian import apply_smoothing, gaussian_mask_7x7, gaussian_mask_15x15

def get_user_choice():
    print("Which function do you want to test?")
    print("1. Correlation")
    print("2. Gaussian Smoothing with 7x7 mask")
    print("3. Gaussian Smoothing with 15x15 mask")
    
    choice = input("Enter the number of your choice: ")
    return choice



choice = get_user_choice()

if choice == "1":
    image = PGMImage()
    image.read_from_file('images/Image.pgm')
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

else:
    print("Invalid choice.")
    exit()