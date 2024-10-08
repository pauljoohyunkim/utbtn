# Underground Transportation Battalion
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# A4 in pixel with 300dpi
A4_SIZE = (3508, 2480)
# Roughly
SQUARE_WIDTH = 20
L_MARGIN = int(2.1 * 2 * SQUARE_WIDTH)
R_MARGIN = int(2.1 * 2 * SQUARE_WIDTH)
T_MARGIN = int(2.97 * 2 * SQUARE_WIDTH)
B_MARGIN = int(2.97 * 2 * SQUARE_WIDTH)

def byte_to_bitstring(byte : int) -> str:
    return bin(byte)[2:].zfill(8)

def bytestring_to_bitstring(bytestring : bytes) -> str:
    return ''.join([byte_to_bitstring(byte) for byte in bytestring])

class UTBTN_Images:
    def __init__(self, size=A4_SIZE, square_width=SQUARE_WIDTH, l_margin=L_MARGIN, r_margin=R_MARGIN, t_margin=T_MARGIN, b_margin=B_MARGIN):
        self.images = []
        self.size = size

        # For encoding bits into UTBTN image
        self.n_space_h = int((A4_SIZE[1] - l_margin - r_margin) / square_width)
        self.n_space_v = int((A4_SIZE[0] - t_margin - b_margin) / square_width)
        self.n_square_per_page = self.n_space_h * self.n_space_v
        self.l_margin = l_margin
        self.r_margin = r_margin
        self.t_margin = t_margin
        self.b_margin = b_margin
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
            rowstart = self.t_margin + rownum * self.square_width
            rowend = rowstart + self.square_width
            colstart = self.l_margin + colnum * self.square_width
            colend = colstart + self.square_width

            self.images[self.pageindex][rowstart:rowend, colstart:colend] = 255 if bit == '0' else 0

            self.bitindex += 1
        
        self.n_bits = self.bitindex
        self.n_pages = self.pageindex + 1
    
    def decode_mode(self):
        self.pageindex = -1
        self.bitindex = 0

    # decode_mode() method MUST be called before usage for the first time!
    # Leaving n_bytes=0 will decode the entire information
    def decode_bytes(self, n_bytes=0, threshold=150) -> bytes:
        if n_bytes == 0:
            n_bytes = self.n_bits // 8
        n_bits_to_read = n_bytes * 8
        n_bits_to_read = min(n_bits_to_read, self.n_bits - self.bitindex)
        if n_bits_to_read == 0:
            return ''

        bitstring = ''
        for i in range(n_bits_to_read):
            if self.bitindex % self.n_square_per_page == 0:
                self.pageindex += 1
            rownum = int((self.bitindex % self.n_square_per_page) / self.n_space_h)
            colnum = (self.bitindex % self.n_square_per_page) % self.n_space_h
            rowstart = self.t_margin + rownum * self.square_width
            rowend = rowstart + self.square_width
            colstart = self.l_margin + colnum * self.square_width
            colend = colstart + self.square_width

            # Get the value of the middle of the square
            pixel_value = self.images[self.pageindex][int((rowstart + rowend) / 2), int((colstart + colend) / 2)]
            # Thresholding
            bit = '0' if pixel_value > threshold else '1'
            bitstring += bit
            self.bitindex += 1

        bytestring = int(bitstring, 2).to_bytes(len(bitstring) // 8, byteorder='big')
        return bytestring
        
