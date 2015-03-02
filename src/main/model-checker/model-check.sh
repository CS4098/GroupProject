#!/bin/bash

# Run Spin in test or verification mode; runs in test (single-path) mode by default

usage="Usage: $0 <path-to-input-PML-file> <path-to-Spin-output-file> [verify]"
promelatmp="modeltest_tmp.promela"
spin="spin"

# Determine path of PML-to-Promela script
scriptdir=(`dirname ${BASH_SOURCE[0]}`)
pmltopromela="$scriptdir/../translator-xml/PMLToPromela.sh"

# Check number of parameters
if [[ "$#" -ne 2 ]] && [[ "$#" -ne 3 ]]; then
	echo $usage
	exit 1
fi

# Check parameters
pmlfile=$1
if ! [[ -f $pmlfile ]]; then
	echo "$usage: given path to input PML file does not exist or is not a regular file."
	exit 1
fi

outputfile=$2
outputdir=(`dirname $outputfile`)
if ! [[ -d $outputdir ]]; then
	mkdir -p $outputdir
fi

# Run translator
$pmltopromela $pmlfile $promelatmp

if ! [[ -f $promelatmp ]]; then
	echo "Error: no Promela file created, exiting."
	exit 1
fi

if [[ "$#" == 2 ]]; then
	# Run Spin in test mode
	$spin $promelatmp > $outputfile 2>&1

elif [[ "$3" == "verify" ]]; then
	# Run Spin in verification mode
	$spin -a $promelatmp

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
	if [[ -f $promelatmp.trail ]]; then
		rm $promelatmp.trail
	fi
fi

# Clean common temporaries
rm $promelatmp
