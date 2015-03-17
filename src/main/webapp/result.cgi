#!/usr/bin/env python
import cgi, cgitb
import os
import subprocess
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
print("div class=\"main\"")

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

print("<p><b>Promela file with resources set:</b>")
print("<p><pre>")
open(promelafile, "w").close()
promela = open(promelafile, "w")
print("<div class=\"code\">")
for line in lines:
    promela.write("%s\n" % line)
    print(line)
print("</div>")
promela.close()
print("</pre>")


spin = subprocess.Popen(["../model-checker/model-check.sh", promelafile, spinfile, "verify"], stdout=subprocess.PIPE)
spin.wait()
for line in spin.stdout:
    print("<p>" + line)

#output spin results
readspin = open(spinfile, "r")
print("<p><b>Spin output:</b><p><pre>")
print("<div class='code' id='spin'>")
print(readspin.read())
print("</div>")
print("</pre>")
readspin.close()
print("</div>")
print("</pre>")

trailfile = promelafile + ".trail"
if os.path.isfile(trailfile):
    trail = subprocess.Popen(["../model-checker/replay-trail.sh", promelafile, trailfile, spinfile], stdout=subprocess.PIPE)
    trail.wait()
    for line in trail.stdout:
        print("<p>" + line)
    #output trail spin results
    readspin = open(spinfile, "r")
    print("<p><b>Spin Trail output:</b><p><pre>")
    print("<div id='spin'>")
    print(readspin.read())
    print("</div>")
    print("</pre>")
    readspin.close()
    print("</div>")
    print("</pre>")

    os.remove(trailfile)

os.remove(spinfile)
os.remove(resourcefilename)
os.remove(promelafile)

print("</div>")
print("</body>")
print("</html>")