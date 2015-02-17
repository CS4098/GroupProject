#!/bin/sh

file=$1

echo "this is the file.sh output, a test script for calling from python cgi\n"

while read line
do
    echo "<p>$line"
done < $file
