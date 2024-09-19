from typing import Union, BinaryIO
from tempfile import SpooledTemporaryFile
import base64
import bz2

def bytes_to_base64_file(data : Union[str, bytes], outputfile : BinaryIO):
    if type(data) == bytes:
    # bytes -> compressed -> base64 encoded
        compressed = bz2.compress(data)
        b64encoded = base64.b64encode(compressed)
        outputfile.write(b64encoded)
    elif type(data) == str:
        compressor = bz2.BZ2Compressor()
        # Write the compressed data to a spooled temporary file
        tf = SpooledTemporaryFile()
        with open(data, "rb") as inputfile:
            # Compression
            data_read = inputfile.read(2**16)
            while data_read:
                compressed = compressor.compress(data_read)
                tf.write(compressed)
                data_read = inputfile.read(2**16)
            compressed = compressor.flush()
            tf.write(compressed)

            # Compressed file to base64 encoding
            tf.seek(0)
            base64.encode(tf, outputfile)
    else:
        raise TypeError('data must be bytes or filename')

def base64_file_to_bytes(inputfile : BinaryIO, outputfile : Union[BinaryIO, None]) -> Union[None, bytes]:
    # Read base64 encoding into compressed file
    tf = SpooledTemporaryFile()
    base64.decode(inputfile, tf)
    tf.seek(0)

    if type(outputfile) == BinaryIO:
        decompressor = bz2.BZ2Decompressor()
        data_read = tf.read(2**16)
        while data_read:
            outputfile.write(decompressor.decompress(data_read))
            data_read = tf.read(2**16)
    elif outputfile == None:
        return bz2.decompress(tf.read())
