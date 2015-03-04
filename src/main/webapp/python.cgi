#!/usr/bin/env python
import cgi, cgitb
import os
import subprocess
import random
import string
import getpass

cgitb.enable()

#html header
print("Content-type: text/html;charset=utf-8\n\n\n")

form = cgi.FieldStorage()
if "pmlfile" not in form:
    print("<H1>Error</H1>")
    print("Please fill in the file field.")
else:
    #currently: saves input file with random filename, passes file to PMLToPromela.sh and outputs the result, then passes through spin and outputs the result, deletes files when finished

    canneda = form["canneda"].value
    if canneda == "on":
        print("<p>")
        print("You've picked a canned predicate!")

    pmlfile = form["pmlfile"]
    resourcea = form["resourcea"]
    resourceb = form["resourceb"]

    #print("<p>file from form: ")    
    #print(pmlfile.filename)

    filename = ""
    promelafile = ""

    #handle input
    if pmlfile.file and pmlfile.filename.endswith(".pml"):
        predicatefilename = "pred.promela"
        predicatefile = open(predicatefilename, 'w')
        predicatefile.write("\n\n");
        if canneda == "on":
            predicatefile.write("never {\n    do\n    :: " + resourcea + " -> break\n    :: true\n    od;\naccept:\n    do\n    :: !" + resourceb + "\n    od\n}")

        while 1:
            basefile = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
            filename = ''.join([basefile, ".pml"])
            if not os.path.exists(filename): break
        promelafile = ''.join(["./", basefile, ".promela"])
        #print("<p>filename: ")
        #print(filename)
        #print("<p>created by user: ")
        #print(getpass.getuser())
        outfile = open(filename, "w")
        while 1:
            line = pmlfile.file.readline()
            if not line: break
            outfile.write(line)
        outfile.close()

        print("<br><br><p>")
        process = subprocess.Popen(["../translator-xml/PMLToPromela.sh", filename, promelafile, predicatefilename], stdout=subprocess.PIPE)
        process.wait()
        for line in process.stdout:
            print(line)

        readpml = open(filename, "r")
        print("<p>PML Input:<p><pre>")
        print(readpml.read())
        print("</pre>")
        readpml.close()

        readpromela = open(promelafile, "r")
        print("<p>Generated Promela:<p><pre>")
        print(readpromela.read())
        print("</pre>")
        readpromela.close()

        spin = subprocess.Popen("spin %s" % promelafile, shell=True, stdout=subprocess.PIPE)
        spin.wait()
        print("<p>Spin output:<p><pre>")
        for line in spin.stdout:
            print(line)
        print("</pre>")

        os.remove(filename)
        os.remove(promelafile)
    
    else:
        print("<p>")
        print("<h1>Please Select a file with a .pml extenstion</h1>")
    




