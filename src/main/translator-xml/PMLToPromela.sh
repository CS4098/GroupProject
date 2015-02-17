#!/bin/bash

usage="Usage: $0 <path-to-input-PML-file> <path-to-output-Promela-file>"
xmltmp="pmltopromela_tmp.xml"

# Determine paths of python components
scriptdir=(`dirname ${BASH_SOURCE[0]}`)
pmltoxml="$scriptdir/PMLToXML.py"
xmltopromela="$scriptdir/XMLToPromela.py"

# Check translators are available
if ! [[ -x $pmltoxml ]] && ! [[ -f $pmltoxml ]]; then
	echo "$Error: PML-to-XML translator missing, exiting."
	exit 1
fi

if ! [[ -x $xmltopromela ]] && ! [[ -f $xmltopromela ]]; then
	echo "$Error: XML-to-Promela translator missing, exiting."
	exit 1
fi

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

promelafile=$2
promeladir=(`dirname $promelafile`)
if ! [[ -d $promeladir ]]; then
	mkdir -p $promeladir
fi

# Run translators
python $pmltoxml -p $pmlfile -x $xmltmp
python $xmltopromela -x $xmltmp -p $promelafile

# Clean temporaries
if [[ -f $xmltmp ]]; then
	rm $xmltmp
fi
