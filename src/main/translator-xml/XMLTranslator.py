#!/usr/bin/env python

from xml.dom import minidom

class XMLTranslator:
    # Parse any other node of the PML file
    def parse_nodes(self, nodes, depth, processes_sofar, process_current, resources_sofar):
        pass

    # Parse Process, the outermost level of a PML file
    def parse_process(self, node):
        processes = [] # List of Promela proctypes
        resources = [] # List of resources

        procname = node.getElementsByTagName("ID")[0].getAttribute("value")
        process_main = ["active proctype " + procname + "()", "{"]
        processes.append(process_main)

        # Parse inner tree nodes
        self.parse_nodes(node.childNodes, 0, processes, process_main, resources)

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

    def translate_xml(self, xml_string):
        xml_tree = minidom.parseString(xml_string)
        print xml_tree.toxml()
        translation = self.parse_process(xml_tree)
        return translation
