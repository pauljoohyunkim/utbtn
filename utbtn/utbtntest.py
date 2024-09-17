import string
import random as rd
from utbtnlib import UTBTN_Images
from utbtn_encode import bytes_to_images
from utbtn_decode import images_to_bytes
from hashlib import sha256
import os

def test1():
    '''Random 5000 bytes ascii, uncompressed'''

    testname = "test1"
    print(f"{testname}: Generating test data")
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

def test2():
    '''Random 5000 bytes ascii, uncompressed'''

    testname = "test2"
    print(f"{testname}: Generating test data")
    data = ''.join(rd.choices(string.ascii_uppercase + string.digits, k=5000)).encode('ascii')

    print(f"{testname}: Encoding data")
    # Encode to images
    images = UTBTN_Images()
    images.encode_bytes(data)

    print(f"{testname}: Decoding data")
    images.decode_mode()
    # Over-Read the images and decode
    data_read = images.decode_bytes(5001)

    print(f"{testname}: {data == data_read}")

def test3():
    '''Random 5000 bytes ascii, compressed, filesave'''

    testname = "test3"
    print(f"{testname}: Generating test file: test.txt")
    data = ''.join(rd.choices(string.ascii_uppercase + string.digits, k=5000)).encode('ascii')
    with open("test1.txt", "wb") as f:
        f.write(data)
    
    # Compute sha256
    m1 = sha256()
    m1.update(data)
    m1_digest = m1.digest()

    print(f"{testname}: Encoding data")
    # Encode to images
    images = bytes_to_images("test1.txt")

    print(f"{testname}: Decoding data")
    images.decode_mode()
    # Over-Read the images and decode
    images_to_bytes(images, "test2.txt")
    
    # Compute sha256 of the newly acquired file
    m2 = sha256()
    with open("test2.txt", "rb") as f:
        m2.update(f.read())
    m2_digest = m2.digest()
    
    print(f"{testname}: {m1_digest == m2_digest}")
    os.remove("test1.txt")
    os.remove("test2.txt")