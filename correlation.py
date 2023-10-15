from image import PGMImage

def correlate(image, mask):
    mask_height = len(mask)
    mask_width = len(mask[0])

    if mask_height % 2 == 0 or mask_width % 2 == 0:
        raise ValueError("Mask dimensions should be odd")

    h = mask_height // 2  # the height and width of the mask are the same, so we only need to calculate h
    correlated_image = PGMImage(image.width, image.height, image.maxval)

    print("Starting correlation...")

    for r in range(image.height):
        if r % 10 == 0:  # Print every 10 rows to reduce the number of print statements
            print(f"Processing row {r}")

        for c in range(image.width):
            sum = 0

            for u in range(-h, h + 1):
                for v in range(-h, h + 1):
                    rr = r + u
                    cc = c + v

                    if 0 <= rr < image.height and 0 <= cc < image.width:
                        sum += mask[u + h][v + h] * image.pixels[rr][cc]

            correlated_image.pixels[r][c] = max(0, min(255, int(sum)))

    print("Correlation completed.")
    return correlated_image
