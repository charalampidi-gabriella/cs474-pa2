from image import PGMImage
from correlation import correlate  

def get_user_choice():
    print("Which function do you want to test?")
    print("1. Correlation")
    
    choice = input("Enter the number of your choice: ")
    return choice

image = PGMImage()
image.read_from_file('images/Image.pgm')

choice = get_user_choice()

if choice == "1":
    small_image = PGMImage()
    small_image.read_from_file('images/Pattern.pgm')
    mask = small_image.pixels  
    print(mask)
    correlated_image = correlate(image, mask)
    new_file_name = 'images/correlated.pgm'
    correlated_image.write_to_file(new_file_name)
    print(f"New image written to {new_file_name}")

else:
    print("Invalid choice.")
    exit()