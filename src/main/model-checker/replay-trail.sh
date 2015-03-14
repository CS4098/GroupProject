#!/bin/bash

### Replay a trail file 

usage="Usage: $0 <path-to-promela-file> <path-to-trail-file> <path-to-spin-output-file>"
spin="spin"

# Check number of parameters
if [[ "$#" -ne 3 ]]; then
	echo $usage
	exit 1
fi

promelafile=$1
trailfile=$2
outputfile=$3

# Check parameters
if ! [[ -f $promelafile ]] || ! [[ -f $trailfile ]]; then
	echo $usage
	exit 1
fi

# Run Spin, following the trail specified
$spin -p $promelafile -k $trailfile > $outputfile 2>&1
