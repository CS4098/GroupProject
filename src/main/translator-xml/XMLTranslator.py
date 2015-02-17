#!/usr/bin/env python

class XMLTranslator:

  # Get display indentation for a certain depth
  def get_indent(self, depth):
    line = ""
    for i in range(0, depth):
      line += "\t"
    return line

  # Get variable id (name)
  def get_varid(self, node):
    return node[0].get("value")

  # Get variables
  def get_vars(self, var):
    vars = []
    for varid in var:
      vars.append(self.get_varid(varid))
    return vars

  # Get variable list used by an action
  def get_varlist(self, node):
    varlist = []
    for var in node.iter("PrimVar"):
      varlist += self.get_vars(var)
    return varlist

  # PML action
  def handle_action(self, node, depth, processes_sofar, process_current, resources_sofar):
    # Blocks (requires)
    reqlist = []
    for req in node.iter("SpecReqs"):
      reqlist[0:] = self.get_varlist(req)
    #print "requires: " + str(reqlist)

    curdepth = depth
    if(len(reqlist) > 0):
      line = self.get_indent(curdepth)
      curdepth += 1
      line += reqlist[0]
      for req in reqlist[1:]:
        line += " && " + req
      line += " ->"
      process_current.append(line)

    # State changes (provides)
    provlist = []
    for prov in node.iter("SpecProv"):
      provlist[0:] = self.get_varlist(prov)
    #print "provides: " + str(provlist)

    if len(provlist) == 1:
      line = self.get_indent(curdepth)
      line += provlist[0] + " = true;"
      process_current.append(line)

    elif len(provlist) > 0:
      process_current.append(self.get_indent(curdepth-1) + "{")
      for prov in provlist:
        line = self.get_indent(curdepth)
        line += prov + " = true;"
        process_current.append(line)        
      process_current.append(self.get_indent(curdepth-1) + "}")

    for req in reqlist:
      resources_sofar.add(req)

    for prov in provlist:
      resources_sofar.add(prov)

  # PML iteration
  def handle_iteration(self, node, depth, processes_sofar, process_current, resources_sofar):
    pass

  # PML sequence
  def handle_sequence(self, node, depth, processes_sofar, process_current, resources_sofar):
    pass

  constructs = {
    "PrimAct" : handle_action,
    "PrimIter" : handle_iteration,
    "PrimSeq" : handle_sequence
    # More..
  }
  # Parse non-Process node of the XML file
  def parse_nodes(self, node, depth, processes_sofar, process_current, resources_sofar):
    for child in node:
      if child.tag in XMLTranslator.constructs:
        XMLTranslator.constructs[child.tag](self, child, depth+1, processes_sofar, process_current, resources_sofar)
    pass

  # Parse Process, the outermost level of a PML file
  def parse_process(self, root):
    processes = [] # List of Promela proctypes
    resources = set() # Set of resources
    procname = root[0].get("value") # Process name; ID is always the first element in well-formed PML

    process_main = ["active proctype " + procname + "()", "{"]
    processes.append(process_main)

    # Parse inner tree nodes
    self.parse_nodes(root, 0, processes, process_main, resources)

    # Add dummy instruction to cope with empty processes
    if len(process_main) <= 2:
      process_main.append("\tskip;")

    process_main.append("}")

    # Assemble resources and processes into translation
    translation = []
    if len(resources) > 0:
      for resource in resources: # FIXME: not sure this is where resources should be going - scoping?
          translation.append("bool " + resource + ";")
      translation.append("")

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
