from utbtnlib import UTBTN_Images
import sys
import argparse
from utbtn_encode import bytes_to_images
from utbtn_decode import process_images_to_utbtn_images, images_to_bytes
from pathlib import Path
from PIL import Image

def main():
    parser = argparse.ArgumentParser(description="Encode/Decode between files and printable images.", epilog="encode: trailing argument should be the filename. decode: trailing arguments should be the filename, and then images.")
    parser.add_argument("action", type=str, help="encode or decode")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args, remainingargs = parser.parse_known_args()

    if args.action not in ["encode", "decode"]:
        parser.print_help()
        sys.exit(1)
    
    if args.action == "encode":
        # There should only be one leftover argument.
        if len(remainingargs) != 1:
            parser.print_help()
            sys.exit(1)
        
        filename = remainingargs[0]
        
        # Encoding
        images = bytes_to_images(filename)
        images.save_all(Path(filename).stem)
        print("Done!")
        
        sys.exit(0)
    elif args.action == "decode":
        # There should be at least two leftover arguments
        # The first argument is the filename
        # The remaining arguments are the image files
        if len(remainingargs) < 2:
            parser.print_help()
            sys.exit(1)

        raw_images = [Image.open(filename) for filename in remainingargs[1:]]
        n_bytes = int(input("n_bytes: "))
        
        images = process_images_to_utbtn_images(raw_images, n_bytes)
        images_to_bytes(images, remainingargs[0])

        sys.exit(0)
    

if __name__ == "__main__":
    main()