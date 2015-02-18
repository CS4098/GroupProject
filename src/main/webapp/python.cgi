#!/usr/bin/env python
import cgi, cgitb
import os
import subprocess
import random
import string
import getpass

cgitb.enable()

#html header
print("Content-type: text/html;charset=utf-8\n\n")

form = cgi.FieldStorage()
if "pmlfile" not in form:
    print("<H1>Error</H1>")
    print("Please fill in the name and file fields.")
else:
    #currently: saves input file with random filename, passes file to file.sh which outputs the contents, deletes file
    pmlfile = form["pmlfile"]
    filename = ""
    if pmlfile.file:
        filename = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
        filename = ''.join([filename, ".pml"])
        print("filename: ")
        print(filename)
        print("<p>created by user: ")
        print(getpass.getuser())
        outfile = open(filename, "w")
        while 1:
            line = pmlfile.file.readline()
            if not line: break
            outfile.write(line)
        outfile.close()
    print("<br><br><p>")
    process = subprocess.Popen(["./file.sh", filename], stdout=subprocess.PIPE)
    process.wait()
    for line in process.stdout:
        print(line)
    os.remove(filename)
    
