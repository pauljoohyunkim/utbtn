# Underground Transportation Battalion
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# A4 in pixel with 300dpi
A4_SIZE = (3508, 2480)
# Roughly
SQUARE_WIDTH = 20
H_MARGIN = int(2.1 * 2 * SQUARE_WIDTH)
V_MARGIN = int(2.97 * 2 * SQUARE_WIDTH)

def byte_to_bitstring(byte : int) -> str:
    return bin(byte)[2:].zfill(8)

def bytestring_to_bitstring(bytestring : bytes) -> str:
    return ''.join([byte_to_bitstring(byte) for byte in bytestring])

class UTBTN_Images:
    def __init__(self, size=A4_SIZE, square_width=SQUARE_WIDTH, h_margin=H_MARGIN, v_margin=V_MARGIN):
        self.images = []
        self.size = size

        # For encoding bits into UTBTN image
        self.n_space_h = int((A4_SIZE[1] - h_margin * 2) / square_width)
        self.n_space_v = int((A4_SIZE[0] - v_margin * 2) / square_width)
        self.n_square_per_page = self.n_space_h * self.n_space_v
        self.h_margin = h_margin
        self.v_margin = v_margin
        self.square_width = square_width

        self.bitindex = 0
        self.pageindex = 0

        self.n_bits = 0
        self.n_pages = 0

    def new_image(self):
        self.images.append(np.ones(self.size, dtype=np.uint8) * 255)
        return len(self.images) - 1

    def add_image(self, image):
        self.images.append(image)

    def show_image(self, i):
        plt.imshow(self.images[i], cmap='gray', vmin=0, vmax=255)

    def save_all(self, filename):
        for i in range(len(self.images)):
            img = Image.fromarray(self.images[i],'L')
            img.save(f'{filename}_{i}.png')

    def encode_bytes(self, data : bytes):
        bits = bytestring_to_bitstring(data)
        for bit in bits:
            if self.bitindex % self.n_square_per_page == 0:
                self.pageindex = self.new_image()

            # Draw square. white for 0, black for 1
            rownum = int((self.bitindex % self.n_square_per_page) / self.n_space_h)
            colnum = (self.bitindex % self.n_square_per_page) % self.n_space_h
            rowstart = self.v_margin + rownum * self.square_width
            rowend = rowstart + self.square_width
            colstart = self.h_margin + colnum * self.square_width
            colend = colstart + self.square_width

            self.images[self.pageindex][rowstart:rowend, colstart:colend] = 255 if bit == '0' else 0

            self.bitindex += 1
        
        self.n_bits = self.bitindex
        self.n_pages = self.pageindex + 1
    
    # This function requires all the configuration filled before using!
    # Including self.n_bits, self.n_pages
    def decode_bytes(self) -> bytes:
        n_bits = self.n_bits
        n_pages = self.n_pages
        pageindex = -1
        for bitindex in range(n_bits):
            if bitindex % self.n_square_per_page == 0:
                pageindex += 1
            rownum = int((self.bitindex % self.n_square_per_page) / self.n_space_h)
            colnum = (self.bitindex % self.n_square_per_page) % self.n_space_h
            rowstart = self.v_margin + rownum * self.square_width
            rowend = rowstart + self.square_width
            colstart = self.h_margin + colnum * self.square_width
            colend = colstart + self.square_width

            # Get the value of the middle of the square
            pixel_value = self.images[pageindex][int((rowstart + rowend) / 2), int((colstart + colend) / 2)]
            # Thresholding
            bit = '0'


        
