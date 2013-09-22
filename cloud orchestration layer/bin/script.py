#!/usr/bin/env python
import os
import sys
if __name__ == '__main__':
	if len(sys.argv) < 4:
		print "Format: ./script.py pm_file image_file vm_type"
		exit(1)
	os.system("chmod 777 script.py")
	os.chdir("../src")
	os.system("python start.py " + sys.argv[1] + " " +sys.argv[2] + " " +sys.argv[3])

