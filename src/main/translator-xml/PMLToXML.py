#!/usr/bin/env/python

import sys
from os.path import isdir, split, abspath
import subprocess


# Read in a pml file and save to an xml file
def translate_pml_file(xml_file, pml_file):

    pml_path = abspath(pml_file.name)
    xml_path = abspath(xml_file)

    # Call XML generator
    # TODO: Remove abs-path
    return_code = subprocess.call("Pmlxml %s %s" % (xml_path, pml_path), shell=True)
    if return_code != 0:
        print "Error occured reading PML file, exiting."
        sys.exit(1)


def valid_xml_path(xml_path):
    path, _ = split(xml_path)
    return isdir(path)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Program to output the ast of a PML program in XML format")
    parser.add_argument('-x', '--xml', required=True, type=str, help="Output abstract syntax tree in XML format")
    parser.add_argument('-p', '--pml', required=True, type=file, help="Input PML file")

    try:
        args = parser.parse_args()
        if valid_xml_path(abspath(args.xml)):
            translate_pml_file(args.xml, args.pml)
        else:
            print "XML path is invalid."
            sys.exit(1)
    except IOError, msg:
        parser.error(str(msg))


if __name__ == "__main__":
    main()
