#!/usr/bin/python

from flask import Flask, render_template, url_for
app = Flask(__name__)

from PIL import Image
#from images2gif import writeGif
from flask import request

import os
import re

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

	@classmethod
	def get_png_file(self, letter):
		if letter.isspace():
			return url_for("static", filename="letters/space.png")
		elif letter == "*":
			return url_for("static", filename="letters/asterisk.png")
		elif letter == ".":
			return url_for("static", filename="letters/period.png")
		elif letter == "&":
			return url_for("static", filename="letters/amp.png")
		elif letter == "$":
			return url_for("static", filename="letters/money.png")
		elif letter == "(":
			return url_for("static", filename="letters/open_paren.png")
		elif letter == ")":
			return url_for("static", filename="letters/close_paren.png")
		elif letter == "#":
			return url_for("static", filename="letters/pound.png")
		elif letter == "?":
			return url_for("static", filename="letters/question.png")
		elif letter == "!":
			return url_for("static", filename="letters/exclamation.png")
		elif letter == "-":
			return url_for("static", filename="letters/dash.png")
		elif letter == "@":
			return url_for("static", filename="letters/at.png")
		else:
			return url_for("static", filename="letters/" + letter + ".png")



@app.route("/", methods=['GET'])
def index():

	css_url = url_for('static', filename='index.css')
	lamp_url = url_for('static', filename='letters/lamp.png')

	bad_input = True
	if "name" in request.args and len(request.args["name"]) > 2 and len(request.args["name"]) < 15:

		bad_input = False

		name = request.args["name"].encode("utf-8").lower()

		first_chunk = name[:-2]
		bounce_letter = name[-2]
		last_letter = name[-1]

		files = []

		regex = re.compile("[a-z]|[()!-@#$&.* ]|[0-9]")
		for letter in name:
			if not regex.match(letter):
				bad_input = True

	if bad_input:

		bad_input = "initial"

		first_chunk = "grav"
		bounce_letter = "i"
		last_letter = "fy"

		first_chunk_url = url_for('static', filename='letters/grav.png')
		bounce_letter_url = url_for('static', filename='letters/i.png')
		last_letter_url = url_for('static', filename='letters/fy.png')

	if not bad_input:


		name = request.args["name"].encode("utf-8").lower()

		print(name)

		Gif_generator.concat_images("static/chunks/" + Gif_generator.extension(name.replace(" ", "").replace("*", "").replace(".", ""), '.png'), \
											[Gif_generator.get_png_file(letter)[1:] for letter in first_chunk])

		first_chunk_url = url_for('static', filename='chunks/' + Gif_generator.extension(name.replace(" ", "").replace("*", "").replace(".", ""), '.png'))
		bounce_letter_url = Gif_generator.get_png_file(bounce_letter)
		last_letter_url = Gif_generator.get_png_file(last_letter)

	return render_template('index.html', css_url=css_url, \
										lamp_url=lamp_url, \
										first_chunk_url=first_chunk_url, \
										bounce_letter_url=bounce_letter_url, \
										last_letter_url=last_letter_url, \
										first_chunk_size=59*len(first_chunk), \
										last_letter_size=59*len(last_letter),
										first_chunk=first_chunk, \
										bounce_letter=bounce_letter, \
										last_letter=last_letter, \
										bad_input=("initial" if (bad_input) else "none"))

if __name__ == "__main__":
	#app.run(host="0.0.0.0", port=int("80"))
	app.run(debug=True)







