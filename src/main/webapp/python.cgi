#!/usr/bin/env python
import cgi, cgitb
import os
import subprocess
import random
import string
import csv
import base64

cgitb.enable()

#html header
print("Content-type: text/html;charset=utf-8\n\n\n")

print("<html>")
print("<head>")
print("<title>CGI Result</title>")
print("<link rel=\"stylesheet\" href=\"../../../css/layout.css\" type=\"text/css\">")
print("</head>")
print("<body>")
print("<div class=\"main\">")

form = cgi.FieldStorage()
if "pmlfile" not in form:
    print("<H1>Error</H1>")
    print("Please fill in the file field.")
else:
    #currently: saves input file with random filename, passes file to PMLToPromela.sh and outputs the result, then passes through spin and outputs the result, deletes files when finished

    pmlfile = form["pmlfile"]

    #handle input
    if pmlfile.file and pmlfile.filename.endswith(".pml"):
        
        #predicatefile = open(predicatefilename, 'w')
        #predicatefile.write("\n\n");
        #if canneda == "on":
        #    predicatefile.write("never {\n    do\n    :: " + str(resourcea) + " -> break\n    :: true\n    od;\naccept:\n    do\n    :: !" + str(resourceb) + "\n    od\n}")

        while 1:
            basefile = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
            filename = basefile + ".pml"
            if not os.path.exists(filename): break
        
        promelafile = basefile + ".promela"
        resourcefilename = basefile + ".csv"

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
            print("<p>" + line)
        
        if pmlcheck:
            print("<br><p><b>pml was not valid :(</b>")
            os.remove(filename)
            raise SystemExit

        #output input pml
        readpml = open(filename, "r")
        print("<p><b>PML File Uploaded by User:</b><p><pre>")
        print("<div class='code' id='pml'>")
        print(readpml.read())
        print("</div>")
        print("</pre>")
        readpml.close()

        #output and encode generated promela
        readpromela = open(promelafile, "r")
        encodedpromela = base64.b64encode(readpromela.read())
        readpromela.seek(0)
        print("<p><b>Initial Promela Generated from the above PML:</b><p><pre>")
        print("<div class='code' id='promela'>")
        print(readpromela.read())
        print("</div>")
        print("</pre>")
        readpromela.close()      

        #output options based on resource file and encode file
        readresources = open(resourcefilename, "r")
        encodedresources = base64.b64encode(readresources.read())
        readresources.seek(0)
        csvreader = csv.reader(readresources)
        resourcelist = list(csvreader)

        print("<form class='main' enctype='multipart/form-data' method='POST' action='result.cgi'>")

        print("<p>Predicates can be specified and tested for:</p>")
        if len(resourcelist) > 0:
            print("<input type='radio' name='predicate' id='nopredicate' value='none' checked> No predicate<br>")
            print("<input type='radio' name='predicate' id='predicate' value='eventually'>")
            print("Resource <select name='eventually'>")
            for resource in resourcelist[0]:
                print("<option id='resource' value=eventually." + resource + ">" + resource + "</option>")
            print("</select> will eventually become available.")



        print("<p>The resources(bools) need to be set to true or false to represent whether they are initially available or not<p><b>Please select starting values for resources below and submit</b><br>")

        if len(resourcelist) > 0:
            for resource in resourcelist[0]:
                print("<i>" + resource + "</i>")
                print("<input type='radio' name=" + resource + " value='true'>True")
                print("<input type='radio' name=" + resource + " value='false' checked>False<br>")


        #pass base64 encoded files to new form
        print("<input name='resourcefile' type='hidden' value=\"" + encodedresources + "\">")
        print("<input name='promelafile' type='hidden' value=\"" + encodedpromela + "\">")
        print("<input name='base' type='hidden' value=\"" + basefile + "\">")
        print("<input type='submit' value='Submit'>")

        print("</form>")
        readresources.close()


        #delete temp files
        os.remove(filename)
        os.remove(resourcefilename)
        os.remove(promelafile)
    else:
        print("<p>")
        print("<h1>Please Select a file with a .pml extenstion</h1>")

print("</div>")
print("</body>")
print("</html>")
