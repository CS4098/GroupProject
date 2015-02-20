#!/bin/bash

# Run Spin in test mode (single path of execution)

usage="Usage: $0 <path-to-input-PML-file> <path-to-Spin-output-file>"
promelatmp="modeltest_tmp.promela"
spin="spin"

# Determine path of PML-to-Promela script
scriptdir=(`dirname ${BASH_SOURCE[0]}`)
pmltopromela="$scriptdir/../translator-xml/PMLToPromela.sh"

# Check number of parameters
if [[ "$#" -ne 2 ]]; then
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

# Run Spin in test mode
$spin $promelatmp > $outputfile 2>&1

# Clean temporaries
if [[ -f $promelatmp ]]; then
	rm $promelatmp
fi
