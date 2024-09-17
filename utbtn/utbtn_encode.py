from utbtnlib import UTBTN_Images
import bz2

# data can be bytes or filename
def bytes_to_image(data : (bytes, str)) -> UTBTN_Images:
  images = UTBTN_Images()

  if type(data) == bytes:
    images.encode_bytes(bz2.compress(data))
  elif type(data) == str:
    with open(data, 'rb') as f:
      comp = bz2.BZ2Compressor()
      data_read = f.read(2 ** 16)
      while data_read:
        images.encode_bytes(comp.compress(data_read))
        data_read = data.read(2**16)
      images.encode_bytes(comp.flush())
  else:
    raise TypeError('data must be bytes or filename')
  return images
