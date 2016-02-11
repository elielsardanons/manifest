#!/usr/bin/env python

from __future__ import print_function
from flask import Flask, render_template
from flask.ext.moment import Moment
from os import listdir
from os.path import isfile, join
import re
from os.path import join, dirname, abspath
import xlrd
import collections

app = Flask(__name__)
moment = Moment(app)
app.debug = True

@app.route("/")
def live():
	xl_workbook = xlrd.open_workbook('/home/eliel/manifest/tandas.xls')
	xl_general = xl_workbook.sheet_by_name('General')
	xl_tandas = xl_workbook.sheet_by_name('Tandas')

	tandas = collections.OrderedDict()
	for col in range(xl_tandas.ncols):
		tandas[col + 1] = []
		for row in xl_tandas.col(col):
			tandas[col + 1].append(row.value)

	nextCall = int(xl_general.cell_value(0,2))
	nextFlight = int(xl_general.cell_value(3,2))

	print("nextCall: " + str(nextCall))
	print("nextFlight: " + str(nextFlight))

	showCount = 4
	showFlights = collections.OrderedDict() 
	skydiverImage = {}
	for tanda in sorted(tandas):
		if (tanda >= nextFlight and showCount > 0):
			showCount = showCount - 1;
			showFlights[tanda] = tandas[tanda]
			for skydiver in tandas[tanda]:
				if isfile('/home/eliel/manifest/static/skydiver/' + str(skydiver).replace(" ", "").lower().rstrip() + '.jpg'):
					skydiverImage[skydiver] = str(skydiver).replace(" ", "").lower().rstrip() + '.jpg'
				else:
					skydiverImage[skydiver] = None
	
	return render_template("showLive.html", showFlights = showFlights, skydiverImage = skydiverImage, nextCall = nextCall) 

if __name__ == "__main__":
	app.run(host = '0.0.0.0', port = 80)
