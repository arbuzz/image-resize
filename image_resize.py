from PIL import Image
import argparse
from os import walk

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Resize all images in direcory'
    )
    parser.add_argument(
        '--input',
        type=str,
        help='Path to dir with images to resize',
        required=True
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Path to dir where result images will be placed',
        required=True
    )
    parser.add_argument(
        '--max',
        type=int,
        help='Max size of larger dimension after resize',
        required=True
    )
    parser.add_argument(
        '--min',
        type=int,
        help='Min size of smaller dimension after resize. Has higher priority than --max',
        required=True
    )

    args = parser.parse_args()

    in_dir = args.input
    out_dir = args.output

    files = []
    for (dirpath, dirnames, filenames) in walk(in_dir):
        files.extend(filenames)
        break

    for f in files:
        try:
            img = Image.open(in_dir + f)
            width = img.size[0]
            height = img.size[1]

            smallest = min(width, height)
            largest = max(width, height)

            k = 1

            if largest > args.max:
                k = args.max / float(largest)

            smallest *= k
            largest *= k

            if smallest < args.min:
                k *= args.min / float(smallest)

            size = width * k, height * k
            img.thumbnail(size, Image.ANTIALIAS)
            img.save(out_dir + f, "JPEG")
        except IOError:
            print "cannot resize image"