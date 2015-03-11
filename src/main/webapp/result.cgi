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

promelafile = form.getvalue("promelafile")
resourcefilename = form.getvalue("resourcefile")

lines = []

readresources = open(resourcefilename, "r")
csvreader = csv.reader(readresources)
resourcelist = list(csvreader)
for resource in resourcelist[0]:
    if resource in form:
        lines.append("bool " + resource + " = " + form.getvalue(resource) + ";")

with open(promelafile, "r") as f:
    base_promela = f.read()
    base_promela = base_promela.split("\n\n")[1]
    lines.append(base_promela)

open(promelafile, "w").close()
promela = open(promelafile, "w")
for line in lines:
    promela.write("%s\n" % line)
    print("<p>" + line + "</p>")
promela.close()



spin = subprocess.Popen("spin %s" % promelafile, shell=True, stdout=subprocess.PIPE)
spin.wait()
print("<p>Spin output:<p><pre>")
print("<div id='spin'>")
for line in spin.stdout:
    print(line)
print("</div>")
print("</pre>")


#os.remove(promelafile)