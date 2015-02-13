#!/usr/bin/env python

import sys
from xml.dom import minidom

def main():
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + " <filename.xml>"
		sys.exit(1)

	filename = sys.argv[1]

	try:
		pmltree = minidom.parse(filename)
		print pmltree.toxml()
	except IOError:
		print "File IO error."

main()