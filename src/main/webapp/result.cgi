#!/usr/bin/env python
import cgi, cgitb
import os
import subprocess
import csv
import base64

cgitb.enable()

#html header
print("Content-type: text/html;charset=utf-8\n\n\n")

form = cgi.FieldStorage()

base = form.getvalue("base")
promelafile = base + ".promela"
spinfile = base + ".spin"
resourcefilename = base + ".csv"

promela = form.getvalue("promelafile")
with open(promelafile, "w") as f:
    promela = base64.b64decode(promela)
    f.write(promela)

resources = form.getvalue("resourcefile")
with open(resourcefilename, "w") as f:
    resources = base64.b64decode(resources)
    f.write(resources)

lines = []

readresources = open(resourcefilename, "r")
csvreader = csv.reader(readresources)
resourcelist = list(csvreader)
if len(resourcelist) > 0:
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

print("<p>Promela file with resources set:")
print("<p><pre>")
open(promelafile, "w").close()
promela = open(promelafile, "w")
for line in lines:
    promela.write("%s\n" % line)
    print(line)
promela.close()
print("</pre>")


spin = subprocess.Popen(["../model-checker/model-check.sh", promelafile, spinfile, "verify"], stdout=subprocess.PIPE)
spin.wait()
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

trailfile = promelafile + ".trail"
os.remove(trailfile) if os.path.isfile(trailfile) else None

os.remove(spinfile)
os.remove(resourcefilename)
os.remove(promelafile)
