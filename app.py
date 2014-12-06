#!/usr/bin/python

from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
def index():
	js_url = url_for('static', filename='index.js')
	css_url = url_for('static', filename='index.css')
	grav_url = url_for('static', filename='grav.png')
	i_url = url_for('static', filename='i.png')
	fy_url = url_for('static', filename='fy.png')
	return render_template('index.html', js_url=js_url, \
										css_url=css_url, \
										grav_url=grav_url, \
										i_url=i_url, \
										fy_url=fy_url)

if __name__ == "__main__":
	app.run(debug=True)