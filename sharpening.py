from gaussian import convolve, gaussian_mask_7x7

def unsharp_masking(image_pixels):
    blurred_image = convolve(image_pixels, gaussian_mask_7x7)
    return [[original - blurred for original, blurred in zip(row1, row2)] for row1, row2 in zip(image_pixels, blurred_image)]

def high_boost_filtering(image_pixels, k):
    blurred_image = convolve(image_pixels, gaussian_mask_7x7)
    mask = [[original - blurred for original, blurred in zip(row1, row2)] for row1, row2 in zip(image_pixels, blurred_image)]
    return [[original + k * boost for original, boost in zip(row1, row2)] for row1, row2 in zip(image_pixels, mask)]
