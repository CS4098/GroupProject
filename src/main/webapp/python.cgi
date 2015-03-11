#!/usr/bin/env python
import cgi, cgitb
import os
import subprocess
import random
import string
import getpass
import csv

cgitb.enable()

#html header
print("Content-type: text/html;charset=utf-8\n\n\n")

form = cgi.FieldStorage()
if "pmlfile" not in form:
    print("<H1>Error</H1>")
    print("Please fill in the file field.")
else:
    #currently: saves input file with random filename, passes file to PMLToPromela.sh and outputs the result, then passes through spin and outputs the result, deletes files when finished

    canneda = ""
    if "canneda" in form:
        canneda = "on"
    if canneda == "on":
        print("<p>")
        print("You've picked a canned predicate!")

    pmlfile = form["pmlfile"]
    resourcea = form["resourcea"]
    resourceb = form["resourceb"]

    filename = ""
    promelafile = ""
    spinfile = ""

    #handle input
    if pmlfile.file and pmlfile.filename.endswith(".pml"):
        resourcefilename = "res.csv"
        #predicatefile = open(predicatefilename, 'w')
        #predicatefile.write("\n\n");
        #if canneda == "on":
        #    predicatefile.write("never {\n    do\n    :: " + str(resourcea) + " -> break\n    :: true\n    od;\naccept:\n    do\n    :: !" + str(resourceb) + "\n    od\n}")
        while 1:
            basefile = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
            filename = ''.join([basefile, ".pml"])
            if not os.path.exists(filename): break
        
        spinfile = ''.join([basefile, ".spin"])
        promelafile = ''.join([basefile, ".promela"]
        resourcefilename = ''.join([basefile, ".csv"]

        #print("<p>filename: ")
        #print(filename)
        #print("<p>created by user: ")
        #print(getpass.getuser())

        #save input file to local temp file
        outfile = open(filename, "w")
        while 1:
            line = pmlfile.file.readline()
            if not line: break
            outfile.write(line)
        outfile.close()

        #run process to translate input pml to promela
        pmlcheck = 0
        process = subprocess.Popen(["../translator-xml/PMLToPromela.sh", filename, promelafile, resourcefilename], stdout=subprocess.PIPE)
        process.wait()
        for line in process.stdout:
            if line:
                pmlcheck = 1
            print("<p>")
            print(line)
        
        if pmlcheck:
            print("<br><p><b>pml was not valid :(</b>")
            raise SystemExit

        #output input pml
        readpml = open(filename, "r")
        print("<p>PML Input:<p><pre>")
        print("<div id='pml'>")
        print(readpml.read())
        print("</div>")
        print("</pre>")
        readpml.close()

        #output generated promela
        readpromela = open(promelafile, "r")
        print("<p>Generated Promela:<p><pre>")
        print("<div id='promela'>")
        print(promelafile)
        print(readpromela.read())
        print("</div>")
        print("</pre>")
        readpromela.close()


        readresources = open(resourcefilename, "r")
        print "<b>Select starting values for resources</b>"
        print "<form class='main' enctype='multipart/form-data' method='POST' action='result.cgi'>"
        csvreader = csv.reader(readresources)
        resourcelist = list(csvreader)
        for resource in resourcelist[0]:
            print "<i>" + resource + "</i>"
            print "<input type='radio' name=" + resource + " value='true'>True"
            print "<input type='radio' name=" + resource + " value='false' checked>False<br>"
        print "<input name='resourcefile' type='hidden' value=\"" + resourcefilename + "\">"
        print "<input name='promelafile' type='hidden' value=\"" + promelafile + "\">"
        print "<input name='spinfile' type='hidden' value=\"" + spinfile + "\">"
        print "<input type='submit' value='Submit'>"

        print "</form>"
        readresources.close()


        #delete temp files
        os.remove(filename)
    else:
        print("<p>")
        print("<h1>Please Select a file with a .pml extenstion</h1>")
