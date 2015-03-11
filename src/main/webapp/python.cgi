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

    canneda = ""
    if "canneda" in form:
        canneda = "on"
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
    spinfile = ""

    #handle input
    if pmlfile.file and pmlfile.filename.endswith(".pml"):
        predicatefilename = "pred.promela"
        predicatefile = open(predicatefilename, 'w')
        predicatefile.write("\n\n");
        if canneda == "on":
            predicatefile.write("never {\n    do\n    :: " + str(resourcea) + " -> break\n    :: true\n    od;\naccept:\n    do\n    :: !" + str(resourceb) + "\n    od\n}")
        #generate random filename for saving files
        while 1:
            basefile = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
            filename = ''.join([basefile, ".pml"])
            if not os.path.exists(filename): break
        
        spinfile = ''.join([basefile, ".spin"])
        promelafile = ''.join([basefile, ".promela"])

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

        #print("<br><br><p>")
        #run process to translate input pml to promela
        pmlcheck = 0
        process = subprocess.Popen(["../translator-xml/PMLToPromela.sh", filename, promelafile, predicatefilename], stdout=subprocess.PIPE)
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
        print(readpromela.read())
        print("</div>")
        print("</pre>")
        readpromela.close()

        #run spin in verify mode on generated promela file
        spin = subprocess.Popen(["../model-checker/model-check.sh", promelafile, spinfile, "verify"], stdout=subprocess.PIPE)
        spin.wait()
        for line in spin.stdout:
            print("<p>")
            print(line)

        #output spin results
        readspin = open(spinfile, "r")
        print("<p>Spin output:<p><pre>")
        print("<div id='spin'>")
        print(readspin.read())
        print("</div>")
        print("</pre>")
        readspin.close()

        #delete temp files
        os.remove(filename)
        os.remove(promelafile)
        os.remove(spinfile)
    else:
        print("<p>")
        print("<h1>Please Select a file with a .pml extenstion</h1>")
    




