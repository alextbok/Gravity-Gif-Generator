#!/usr/bin/env python

from __future__ import print_function
from PIL import Image, ImageChops
from PIL.GifImagePlugin import getheader, getdata


def makedelta(fp, sequence):
    """Convert list of image frames to a GIF animation file"""

    frames = 0

    previous = None

    for im in sequence:

    	print("ONE ITERATION")
        #
        # FIXME: write graphics control block before each frame

        if not previous:

            # global header
            #print(getheader(im))
            #print(getdata(im))
            #for s in getheader(im) + getdata(im):
            #    fp.write(s)
            for elt in getheader(im):
            	if elt:
            		for s in elt:
            			fp.write(s)
            for elt in getdata(im):
            	if elt:
            		for s in elt:
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
		print("Usage: gif_create infile outfile ")
		sys.exit(1)

	sequence = []
	for i in range(2, len(sys.argv)):
		im = Image.open(sys.argv[i])
		if im.mode != 'RGBA':
			print("BAD")
			im = im.convert('RGBA')
		else:
			print("GOOD")
		sequence.append(im)


	# generate sequence
	#for i in range(100):
	#	im = <generate image i>
	#	sequence.append(im)

	outfile = open(sys.argv[1], "wb")
	makedelta(outfile, sequence)
	outfile.close()












