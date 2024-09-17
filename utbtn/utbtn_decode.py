from PIL import Image
import numpy as np
from utbtnlib import UTBTN_Images, A4_SIZE, SQUARE_WIDTH, L_MARGIN, R_MARGIN, T_MARGIN, B_MARGIN
from typing import Union
import bz2

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
def process_images_to_utbtn_images(raw_images : list, n_bytes, size=A4_SIZE, square_width=SQUARE_WIDTH, l_margin=L_MARGIN, r_margin=R_MARGIN, t_margin=T_MARGIN, b_margin=B_MARGIN) -> UTBTN_Images:
    images = UTBTN_Images()
    images.n_bits = n_bytes * 8
    images.size = size
    images.square_width=square_width
    images.l_margin=l_margin
    images.r_margin=r_margin
    images.t_margin=t_margin
    images.b_margin=b_margin
    images.n_pages = len(raw_images)

    for raw_image in raw_images:
        resized_image = np.array(raw_image.resize((images.size[1], images.size[0])), dtype=np.uint8)
        images.images.append(resized_image)

    return images

def detect_box(image : np.ndarray, threshold=150):
    thresholded_image = np.vectorize(lambda x : 255 if x < threshold else 0)(image).astype(np.uint8)

