import string
import random as rd
from utbtnlib import UTBTN_Images

def test1():
    '''Random 5000 bytes ascii, uncompressed'''

    testname = "test1"
    print(f"{testname}: Generating test data:")
    data = ''.join(rd.choices(string.ascii_uppercase + string.digits, k=5000)).encode('ascii')

    print(f"{testname}: Encoding data")
    # Encode to images
    images = UTBTN_Images()
    images.encode_bytes(data)

    print(f"{testname}: Decoding data")
    images.decode_mode()
    # Read the images and decode
    data_read = images.decode_bytes(5000)

    print(f"{testname}: {data == data_read}")