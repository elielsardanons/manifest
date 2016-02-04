#!/usr/bin/env python

from flask import Flask, render_template
from flask.ext.moment import Moment
from os import listdir
from os.path import isfile, join
import re

app = Flask(__name__)
moment = Moment(app)
app.debug = True

@app.route("/")
def live():
	mypath = 'flights'
	flights = [f for f in listdir(mypath) if isfile(join(mypath, f))]

	flying = file('flying').read()

	lastflights = {}
	skydiverImage = {}

	showCount = 0
	for flight in sorted(flights):
		if int(re.search(r'\d+', flight).group()) < int(flying):
			continue
		print flight
		showCount = showCount + 1
		with file(join(mypath, flight)) as f:
			s = f.readlines()
			lastflights[flight] = s
			for skydiver in s:
				if isfile('/home/eliel/manifest/static/skydiver/' + skydiver.replace(" ", "%20").lower().rstrip() + '.jpg'):
					skydiverImage[skydiver] = skydiver
				else:
					skydiverImage[skydiver] = None
		if showCount == 4:
			break

	return render_template("showLive.html", flights = lastflights, flightNum = int(flying), skydiverImage = skydiverImage)

if __name__ == "__main__":
	app.run()
