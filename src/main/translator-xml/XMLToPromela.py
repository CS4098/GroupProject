#!/usr/bin/env/python

import sys
import XMLTranslator

# Read in an XML file representing an AST and output the corresponding Promela file
def translate_xml_file(input_filename, output_filename):

  # Handle input file
  try:
    xml_file = open(input_filename, 'r')
    xml_string = xml_file.read()
    xml_file.close()

  except IOError:
    print "Error processing input file, exiting."
    sys.exit(1)

  # Perform translation
  translator = XMLTranslator.XMLTranslator()
  translation = translator.translate_xml(xml_string)

  # Handle output file
  try:
    # Read XML file
    promela_file = open(output_filename, 'w')
    for line in translation:
      promela_file.write(line + '\n')
    promela_file.close()

  except IOError:
    print "Error processing output file, exiting."
    sys.exit(1)
