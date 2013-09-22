#!/usr/bin/python
from flask import Flask
import get
import requests
from requests import server
import sys

app=Flask(__name__)
app.register_blueprint(server,url_prefix='/server')

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Format: python filename.py pm_file image_file vmType"
		exit(1)

	get.get_machines(sys.argv[1])
	get.get_images(sys.argv[2])
	get.parse_vmtype(sys.argv[3])
	get.get_imagename()
	app.run(debug=True)



