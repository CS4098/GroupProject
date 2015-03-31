#!/usr/bin/env python
import lxml
import sys
from lxml import etree
MAX_ITERATIONS = 4  # Engineers induction as suggested by A Butterfield


class XMLTranslator:

    def __init__(self):
        self.constructs = {
            "PrimAct": self.handle_action,
            "PrimBr": self.handle_branch,
            "PrimIter": self.handle_iteration,
            "PrimSeln": self.handle_selection,
            "PrimSeq": self.handle_sequence,
            "PrimTask": self.handle_sequence
        }
        self.anon_index = 1
        self.proccount_index = 1

    # Get display indentation for a certain depth
    @staticmethod
    def get_indent(depth):
        line = ""
        for i in range(0, depth):
            line += "\t"
        return line

    # Get variable id (name)
    @staticmethod
    def get_varid(node):
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
        # print "requires: " + str(reqlist)

        curdepth = depth
        if len(reqlist) > 0:
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
        # print "provides: " + str(provlist)

        if len(provlist) == 1:
            line = self.get_indent(curdepth)
            line += provlist[0] + " = true;"
            process_current.append(line)

        elif len(provlist) > 0:
            process_current.append(self.get_indent(curdepth - 1) + "{")
            for prov in provlist:
                line = self.get_indent(curdepth)
                line += prov + " = true;"
                process_current.append(line)
            process_current.append(self.get_indent(curdepth - 1) + "}")

        for req in reqlist:
            resources_sofar.add(req)

        for prov in provlist:
            resources_sofar.add(prov)

    # PML branch
    def handle_branch(self, node, depth, processes_sofar, process_current, resources_sofar):
        # Where a branch construct is named, we will use that name as process-counting variable name; otherwise, assign a default name
        construct_name = ""
        counter_name = "proc_count_" + str(self.proccount_index)
        if node[0] is not None and node[0].tag == "OpNmId":
            construct_name = node[0][0].get("value")  # Branch name; ID will be first element in well-formed XML
            counter_name = construct_name
        else:
            self.proccount_index += 1

        beforeline = self.get_indent(depth)
        beforeline += "int " + str(counter_name) + " = _nr_pr;"  # Records the number of processes currently running
        process_current.append(beforeline)

        for child in node:
            if child.tag != "OpNmId" and child.tag != "OpNmNull":  # Not interested in the ID again

                # Where a nested construct is named, we will use that name as the spawned proctype name; otherwise, assign a default name
                branch_name = "anon_proctype_" + str(self.anon_index)
                if child.tag == "PrimAct":
                    branch_name = str(child[0].get("value"))
                elif child[0] is not None and child[0].tag == "OpNmId":
                    branch_name = str(child[0][0].get("value"))
                else:
                    self.anon_index += 1

                process_within = ["proctype " + branch_name + "()", "{"]
                processes_sofar.append(process_within)

                if child.tag == "PrimAct":  # Action blocks work slightly differently
                    self.parse_node_as_branch(node, 0, processes_sofar, process_within, resources_sofar, branch_name)
                elif child.tag in self.constructs:
                    self.constructs[child.tag](child, 1, processes_sofar, process_within, resources_sofar)

                process_within.append("}")
                runline = self.get_indent(depth)
                runline += "run " + branch_name + "();"
                process_current.append(runline)

        afterline = self.get_indent(depth)
        afterline += "_nr_pr == " + str(counter_name) + " ->"  # Waits until the spawned processes have completed
        process_current.append(afterline)

    # PML iteration
    def handle_iteration(self, node, depth, processes_sofar, process_current, resources_sofar):
        count = "count_" + ("_" * depth)
        line = "%sint %s;" % (self.get_indent(depth), count)
        process_current.append(line)
        line = "%sfor (%s : 1 .. %d) {" % (self.get_indent(depth), count, MAX_ITERATIONS)
        process_current.append(line)
        self.parse_nodes(node, depth, processes_sofar, process_current, resources_sofar)
        line = "%s}" % self.get_indent(depth)
        process_current.append(line)

    # PML sequence
    def handle_sequence(self, node, depth, processes_sofar, process_current, resources_sofar):
        self.parse_nodes(node, depth, processes_sofar, process_current, resources_sofar)

    # Parse non-Process node of the XML file
    def parse_nodes(self, node, depth, processes_sofar, process_current, resources_sofar):
        for child in node:
            if child.tag in self.constructs:
                self.constructs[child.tag](child, depth + 1, processes_sofar, process_current, resources_sofar)

    # Parse child node of a branch construct
    def parse_node_as_branch(self, node, depth, processes_sofar, process_current, resources_sofar, branch_name):
        for child in node:
            if child.tag != "OpNmId" and child.tag != "OpNmNull":
                if child[0].get("value") == branch_name:
                    if child.tag in self.constructs:
                        self.constructs[child.tag](child, depth + 1, processes_sofar, process_current, resources_sofar)

    # Parse Process, the outermost level of a PML file
    def parse_process(self, root):
        processes = []  # List of Promela proctypes
        resources = set()  # Set of resources
        procname = root[0].get("value")  # Process name; ID is always the first element in well-formed PML

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

        resources_ordered = list(resources)
        resources_ordered.sort()

        resourcelist = []
        if len(resources) > 0:
            for i, resource in enumerate(resources_ordered):  # FIXME: not sure this is where resources should be going - scoping?
                if i < len(resources) - 1:
                    resourcelist.append(resource + ",")
                else:
                    resourcelist.append(resource)
            resourcelist.append("")
        translation.append(resourcelist)

        processlist = []
        for process in processes:
            for line in process:
                processlist.append(line)
            processlist.append("")
        translation.append(processlist)

        return translation

    # PML selection
    def handle_selection(self, node, depth, processes_sofar, process_current, resources_sofar):
        if_block = False
        curdepth = depth
        line = self.get_indent(curdepth)
        for child_node in node.iterchildren():
            if child_node.tag in self.constructs:
                if not if_block:
                    if_block = not if_block
                    process_current.append(line + "if")
                process_current.append(line + ":: true ->")
                temp_root = etree.Element(child_node.tag)
                temp_root.insert(0, child_node)
                self.parse_nodes(temp_root, depth + 1, processes_sofar, process_current, resources_sofar)
        if if_block:
            process_current.append(line + "fi")

    def translate_xml(self, xml_string):

        root = None
        try:
            root = lxml.etree.fromstring(xml_string)
        except lxml.etree.XMLSyntaxError:
            print "Error parsing XML, exiting."
            sys.exit(1)

        translation = self.parse_process(root)

        return translation
