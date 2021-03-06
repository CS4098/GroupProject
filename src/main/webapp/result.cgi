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
print("<div class=\"main\">")

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
    split_promela = base_promela.split("\n\n", 2)
    if len(split_promela) is 3:
        base_promela = split_promela[1] + "\n\n" + split_promela[2]
    lines.append(base_promela)

print("<p><b>Generated Promela file updated with user defined resources:</b>")
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

predicate = form.getvalue("predicate")
if predicate == "none":
    print("<p id='nopredicate'>No predicate selected.</p>")
    spin = subprocess.Popen(["../model-checker/model-check.sh", promelafile, spinfile, "verify"], stdout=subprocess.PIPE)
elif predicate == "eventually":
    predresource = form.getvalue("eventually").split(".")[1]
    pred = ("!(<> ", predresource, ")")
    predparam = ''.join(pred)
    print("<p id='predicate'>Predicate selected: " + predparam + "</p>")
    spin = subprocess.Popen(["../model-checker/model-check.sh", promelafile, spinfile, predparam, "verify"], stdout=subprocess.PIPE)

spin.wait()
for line in spin.stdout:
    print("<p>" + line)           
trailfile = promelafile + ".trail"
trailexists = os.path.isfile(trailfile)
if trailexists:
    print("<div class=\"incorrect\"><p>Spin found errors in the model, results are shown below</p></div>")
else:
    print("<div class=\"correct\"><p>Spin has found no issues, results are shown below</p></div>")

#output spin results
readspin = open(spinfile, "r")
print("<p><b>Spin Output for the Promela file:</b><p><pre>")
print("<div class='code' id='spin'>")
print(readspin.read())
print("</div>")
print("</pre>")
readspin.close()
print("</pre>")

if trailexists:
    trail = subprocess.Popen(["../model-checker/replay-trail.sh", promelafile, trailfile, spinfile], stdout=subprocess.PIPE)
    trail.wait()
    for line in trail.stdout:
        print("<p>" + line)
    #output trail spin results
    readspin = open(spinfile, "r")
    print("<p><b>Spin Output for the Promela Trail file generated by the initial Spin run:</b><p><pre>")
    print("<div class='code' id='spintrail'>")
    print(readspin.read())
    print("</div>")
    print("</pre>")
    readspin.close()
    print("</pre>")

    os.remove(trailfile)

os.remove(spinfile)
os.remove(resourcefilename)
os.remove(promelafile)

print("</div>")
print("</body>")
print("</html>")
