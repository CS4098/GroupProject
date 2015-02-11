#!/usr/bin/env python
import cgi, cgitb
cgitb.enable()

print "Content-type: text/html;charset=utf-8\n\n"

form = cgi.FieldStorage()
if "name" not in form or "pmlfile" not in form:
    print "<H1>Error</H1>"
    print "Please fill in the name and file fields."
else:
    print "<p>name:", form["name"].value
    print "<p>file:", form["pmlfile"].value
    
