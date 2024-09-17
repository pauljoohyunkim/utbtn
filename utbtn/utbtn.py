from utbtnlib import UTBTN_Images
import sys
import argparse
from utbtn_encode import bytes_to_images
from utbtn_decode import images_to_bytes
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Encode/Decode between files and printable images.", epilog="encode: trailing argument should be the filename.decode: trailing arguments should be images.")
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

        sys.exit(0)
    

if __name__ == "__main__":
    main()