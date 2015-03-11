#!/usr/bin/env/python

import sys
import XMLTranslator


# Read in an XML file representing an AST and output the corresponding Promela file
def translate_xml_file(xml_file, resource_file, promela_file):

    # Handle input file
    try:
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
        for line in translation[0]:
            resource_file.write(line)
        resource_file.close()

        for line in translation[1]:
            promela_file.write(line + '\n')
        promela_file.close()

    except IOError:
        print "Error processing output file, exiting."
        sys.exit(1)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="XML to promela code translator")
    parser.add_argument('-x', '--xml', required=True, type=file, help="Input abstract syntax tree in XML format")
    parser.add_argument('-r', '--txt', required=True, type=argparse.FileType('w'), help="Output resources file")
    parser.add_argument('-p', '--pl', required=True, type=argparse.FileType('w'), help="Output promela file")

    try:
        args = parser.parse_args()
        translate_xml_file(args.xml, args.txt, args.pl)
    except IOError, msg:
        parser.error(str(msg))


if __name__ == "__main__":
    main()
