#!/usr/bin/env python

from __future__ import print_function
from PIL import Image, ImageChops
from PIL.GifImagePlugin import getheader, getdata

sequence = []

# generate sequence
for i in range(100):
	im = <generate image i>
	sequence.append(im)

# write GIF animation
fp = open("out.gif", "wb")
gifmaker.makedelta(fp, sequence)
fp.close()


def makedelta(fp, sequence):
    """Convert list of image frames to a GIF animation file"""

    frames = 0

    previous = None

    for im in sequence:

        #
        # FIXME: write graphics control block before each frame

        if not previous:

            # global header
            for s in getheader(im) + getdata(im):
                fp.write(s)

        else:

            # delta frame
            delta = ImageChops.subtract_modulo(im, previous)

            bbox = delta.getbbox()

            if bbox:

                # compress difference
                for s in getdata(im.crop(bbox), offset = bbox[:2]):
                    fp.write(s)

            else:
                # FIXME: what should we do in this case?
                pass

        previous = im.copy()

        frames += 1

    fp.write(";")

    return frames


if __name__ == "__main__":

    import sys

    if len(sys.argv) < 3:
        print("GIFMAKER -- create GIF animations")
        print("Usage: gifmaker infile outfile")
        sys.exit(1)

    compress(sys.argv[1], sys.argv[2])