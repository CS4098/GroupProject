#!/usr/bin/env python

import sys
from xml.dom import minidom

def main():
	if len(sys.argv) < 3:
		print "Usage: " + sys.argv[0] + " <input-filename.xml> <output-filename.pml>"
		sys.exit(1)

	input_filename = sys.argv[1]

	try:
		pmltree = minidom.parse(input_filename)
		print pmltree.toxml()
	except IOError:
		print "File IO error."

main()