#!/bin/bash

# Run Spin in test or verification mode; runs in test (single-path) mode by default

usage="Usage: $0 <path-to-input-Promela-file> <path-to-Spin-output-file> [verify]"
spin="spin"

# Check number of parameters
if [[ "$#" -ne 2 ]] && [[ "$#" -ne 3 ]]; then
	echo $usage
	exit 1
fi

# Check parameters
promelafile=$1
if ! [[ -f $promelafile ]]; then
	echo "$usage: given path to input Promela file does not exist or is not a regular file."
	exit 1
fi

outputfile=$2
outputdir=(`dirname $outputfile`)
if ! [[ -d $outputdir ]]; then
	mkdir -p $outputdir
fi

if [[ "$#" == 2 ]]; then
	# Run Spin in test mode
	$spin $promelafile > $outputfile 2>&1

elif [[ "$3" == "verify" ]]; then
	# Run Spin in verification mode
	$spin -a $promelafile

	if ! [[ -f "pan.c" ]]; then
		echo "Error: no pan.c file generated, exiting."
		exit 1
	fi

	gcc -O2 -DSAFETY -o pan pan.c

	if ! [[ -x "pan" ]]; then
		echo "Error: no pan executable generated, exiting."
		exit 1
	fi

	./pan > $outputfile 2>&1

	# Clean temporaries relating to verification mode
	rm pan.? pan

	# FIXME: maybe do something with the trail files later; for now, erase this artefact
	if [[ -f $promelafile.trail ]]; then
		rm $promelafile.trail
	fi
fi
