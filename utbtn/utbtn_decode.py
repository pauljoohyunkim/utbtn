from PIL import Image
from utbtnlib import UTBTN_Images
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
