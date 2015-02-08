#!/bin/bash

usage="Usage: runner <path-to-binary> <path-to-test-dir>"

# Check number of parameters
if [[ "$#" -ne 2 ]]; then
	echo $usage
	exit 1
fi

# Check first parameter is the path to an executable file
translator=$1
if ! [[ -x $translator ]] || [[ -d $translator ]]; then
	echo "$usage: given path to binary is not an executable file."
	exit 1
fi

# Check the second parameter is the path to a directory
suite=$2
if ! [[ -d $suite ]]; then
	echo "$usage: given path to test-suite is not a directory."
	exit 1
fi

for dir in $2/*/
do
	echo $dir
	for file in $dir/*
	do
		echo $file
	done
done
