from PIL import Image
import numpy as np
from utbtnlib import UTBTN_Images, A4_SIZE, SQUARE_WIDTH, L_MARGIN, R_MARGIN, T_MARGIN, B_MARGIN
from typing import Union
import bz2
#import pdb

# if output is a string, then it will be saved as a file
# if kept as None, then it will return the bytes
def images_to_bytes(images : UTBTN_Images, output=Union[None, str]) -> Union[bytes, None]:
    if output == None:
        images.decode_mode()
        bytestring = images.decode_bytes()
        data = bz2.decompress(bytestring)
        return data
    elif type(output) == str:
        with open(output, "wb") as f:
            decomp = bz2.BZ2Decompressor()
            images.decode_mode()
            data_read = images.decode_bytes(2**16)
            while data_read:
                f.write(decomp.decompress(data_read))
                data_read = images.decode_bytes(2**16)

# Given a list of PIL images
def process_images_to_utbtn_images(raw_images : list, n_bytes, n_space_h, n_space_v, size=A4_SIZE) -> UTBTN_Images:
    images = UTBTN_Images()
    images.n_bits = n_bytes * 8
    images.size = size
    images.n_space_h = n_space_h
    images.n_space_v = n_space_v
    images.n_square_per_page = n_space_h * n_space_v

    images.n_pages = len(raw_images)
    images.l_t_margins = []

    for i in range(len(raw_images)):
        raw_image = raw_images[i]
        if i == 0:
            images.l_margin = int(input("Image 0 left margin (cm): ")) * 300 / 2.54
            images.r_margin = int(input("Image 0 right margin (cm): ")) * 300 / 2.54
            images.t_margin = int(input("Image 0 top margin (cm): ")) * 300 / 2.54
            images.b_margin = int(input("Image 0 bottom margin (cm): ")) * 300 / 2.54
            images.square_width_h = (size[1] - images.l_margin - images.r_margin) / n_space_h
            images.square_width_v = (size[0] - images.t_margin - images.b_margin) / n_space_v
        else:
            images.l_margin = int(input("Image 0 left margin (cm): ")) * 300 / 2.54
            images.t_margin = int(input("Image 0 top margin (cm): ")) * 300 / 2.54
        images.l_t_margins.append((images.l_margin, images.t_margin))

        resized_image = np.array(raw_image.resize((images.size[1], images.size[0])), dtype=np.uint8)
        images.images.append(resized_image)

    return images

# Due to compression, it is unlikely that a whole row or column is zero for usual files.
def detect_box(image : np.ndarray, pixel_threshold=150, ignore_first=40):
    n_row, n_col = image.shape
    # For computation, black = 1, white = 0
    thresholded_image = np.vectorize(lambda x : 1 if x < pixel_threshold else 0)(image).astype(np.float16)

    # Detect left and right edge
    left_kernel = np.zeros((n_row, 3))
    left_kernel[:,0] = -1
    left_kernel[:,2] = 1
    left_convolutions = [0] + [weighted_sum(left_kernel, thresholded_image[:,i-1:i+2]) for i in range(1, n_col-1)] + [0]
    for i in range(n_col):
        if i < ignore_first:
            continue
        if left_convolutions[i] != 0:
            break
    l_margin = i+1
    for j in range(n_col):
        if j < ignore_first:
            continue
        if left_convolutions[n_col-j-1] != 0:
            break
    r_margin = j+1

    # Detect top and bottom edge
    top_kernel = np.zeros((3, n_col))
    top_kernel[0,:] = -1
    top_kernel[2,:] = 1
    top_convolutions = [0] + [weighted_sum(top_kernel, thresholded_image[i-1:i+2,:]) for i in range(1, n_row-1)] + [0]
    for i in range(n_row):
        if i < ignore_first:
            continue
        if top_convolutions[i] != 0:
            break
    t_margin = i+1
    for j in range(n_row):
        if j < ignore_first:
            continue
        if top_convolutions[n_row-j-1] != 0:
            break
    b_margin = j+1

    return (l_margin, r_margin, t_margin, b_margin)

def weighted_sum(kernel : np.ndarray, mat : np.ndarray):
    return np.dot(kernel.flatten(), mat.flatten())
