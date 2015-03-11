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
spinfile = promelafile + ".spin"
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
    base_promela = base_promela.split("\n\n")
    if len(base_promela) is 2:
        base_promela = base_promela[1]
    else:
        base_promela = base_promela[0]
    lines.append(base_promela)

open(promelafile, "w").close()
promela = open(promelafile, "w")
for line in lines:
    promela.write("%s\n" % line)
    print("<p>" + line + "</p>")
promela.close()



spin = subprocess.Popen(["../model-checker/model-check.sh", promelafile, spinfile, "verify"], stdout=subprocess.PIPE)
spin.wait()
print("<p>Spin output:<p><pre>")
print("<div id='spin'>")
for line in spin.stdout:
    print(line)
#output spin results
readspin = open(spinfile, "r")
print("<p>Spin output:<p><pre>")
print("<div id='spin'>")
print(readspin.read())
print("</div>")
print("</pre>")
readspin.close()
print("</div>")
print("</pre>")


#os.remove(promelafile)