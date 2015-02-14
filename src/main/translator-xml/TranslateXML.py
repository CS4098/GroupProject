#!/usr/bin/env python

import sys
from xml.dom import minidom

# Parse any other node of the PML file
def parse_nodes(nodes, depth, processes_sofar, process_current, resources_sofar):
  pass

# Parse Process, the outermost level of a PML file
def parse_process(node):
  processes = [] # List of Promela proctypes
  resources = [] # List of resources

  procname = node.getElementsByTagName("ID")[0].getAttribute("value")
  process_main = ["active proctype " + procname + "()", "{"]
  processes.append(process_main)

  # Parse inner tree nodes
  parse_nodes(node.childNodes, 0, processes, process_main, resources)

  process_main.append("}")

  # Assemble resources and processes into translation
  translation = []
  '''
  for resource in resources: # FIXME: not sure this is where resources should be going - scoping?
    translation.append(resource)
  translation.append("")
  '''
  for process in processes:
    for line in process:
      translation.append(line)

  return translation

# Main
def main():
  if len(sys.argv) < 3:
    print "Usage: " + sys.argv[0] + " <input-filename.xml> <output-filename.pml>"
    sys.exit(1)

  input_filename = sys.argv[1]
  output_filename = sys.argv[2]

  try:
    # Read in XML
    pmltree = minidom.parse(input_filename)
    print pmltree.toxml()

    # Translate XML tree to Promela listing
    translation = parse_process(pmltree)
    print translation

    # Print out Promela listing
    outfile = open(output_filename, "w")
    for line in translation:
      outfile.write(line + "\n")
    outfile.close()

  except IOError:
    print "File IO error."

main()