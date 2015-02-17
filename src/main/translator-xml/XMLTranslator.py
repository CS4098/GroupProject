#!/usr/bin/env python

class XMLTranslator:

  # Parse non-Process node of the XML file
  def parse_nodes(self, nodes, depth, processes_sofar, process_current, resources_sofar):
    for child in nodes:
      print child.tag        
    pass

  # Parse Process, the outermost level of a PML file
  def parse_process(self, root):
    processes = [] # List of Promela proctypes
    resources = [] # List of resources
    procname = root[0].get("value") # Process name; ID is always the first element in well-formed PML

    process_main = ["active proctype " + procname + "()", "{"]
    processes.append(process_main)

    # Parse inner tree nodes
    self.parse_nodes(root, 0, processes, process_main, resources)

    process_main.append("}")

    # Assemble resources and processes into translation
    translation = []
    #for resource in resources: # FIXME: not sure this is where resources should be going - scoping?
    #    translation.append(resource)
    #translation.append("")

    for process in processes:
      for line in process:
        translation.append(line)

    return translation

  def translate_xml(self, xml_string):
    from lxml import etree
    root = etree.fromstring(xml_string)
    print etree.tostring(root)
    print "-------"
    translation = self.parse_process(root)
    return translation
