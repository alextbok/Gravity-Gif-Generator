#!/usr/bin/python

from flask import Flask, render_template, url_for
app = Flask(__name__)

from PIL import Image
from images2gif import writeGif
from flask import request

import os

#parameters for gif tuning
FRAMES = 2
FRAME_DELAY = 0.75
WIDTH, HEIGHT = 600, 600

class Gif_generator(object):

	@classmethod
	def create_gif(self, outfile, *args):
		'''
		Creates a gif from the arg files and saves it to outfile
		'''
		frames = []
		for img in args:
			frames.append( Image.open(img) )
		outfile = Gif_generator.extension(outfile, ".gif")
		writeGif(outfile, frames, duration=FRAME_DELAY, dither= 0)

	@classmethod
	def concat_images(self, outfile, args):
		'''
		Concatenates our pngs horizontally (images must all be same height)
		'''
		img = Image.open(args[0])
		new_image = Image.new("RGBA", (sum([Image.open(f).size[0] for f in args]), img.size[1]))

		x = 0
		for i in range(len(args)):
			img = Image.open(args[i])
			new_image.paste(img, (x, 0) )
			x += img.size[0]

		new_image.save( Gif_generator.extension(outfile, ".png") )

	@classmethod
	def extension(self, fname, ext):
		if not fname.endswith(ext):
			if fname.find(".") >= 0:
				fname = ( fname[:fname.find(".")] + ext )
			else:
				fname += ext
		return fname


@app.route("/", methods=['GET'])
def index():



	js_url = url_for('static', filename='index.js')
	css_url = url_for('static', filename='index.css')
	lamp_url = url_for('static', filename='letters/lamp.png')

	if not "name" in request.args or len(request.args["name"]) < 3 or len(request.args["name"]) > 10:

		first_chunk = "grav"
		bounce_letter = "i"
		last_letter = "fy"
		first_chunk_url = url_for('static', filename='letters/grav.png')
		bounce_letter_url = url_for('static', filename='letters/i.png')
		last_letter_url = url_for('static', filename='letters/fy.png')

	else:

		name = request.args["name"].encode("utf-8").lower()

		first_chunk = name[:-2]
		bounce_letter = name[-2]
		last_letter = name[-1]

		Gif_generator.concat_images("static/chunks/" + name, [("static/letters/" + letter + ".png") for letter in first_chunk])

		first_chunk_url = url_for('static', filename='chunks/' + name + '.png')
		bounce_letter_url = url_for('static', filename='letters/' + bounce_letter + '.png')
		last_letter_url = url_for('static', filename='letters/' + last_letter + '.png')

	return render_template('index.html', js_url=js_url, \
										css_url=css_url, \
										lamp_url=lamp_url, \
										first_chunk_url=first_chunk_url, \
										bounce_letter_url=bounce_letter_url, \
										last_letter_url=last_letter_url, \
										first_chunk_size=59*len(first_chunk), \
										last_letter_size=59*len(last_letter),
										first_chunk=first_chunk, \
										bounce_letter=bounce_letter, \
										last_letter=last_letter)

if __name__ == "__main__":
	app.run(debug=True)







