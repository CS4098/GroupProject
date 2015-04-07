#!/bin/bash

# Run Spin in test or verification mode; runs in test (single-path) mode by default

usage="Usage: $0 <path-to-input-Promela-file> <path-to-Spin-output-file> [verify]"
spin="spin"
pan="pan"
cc="gcc"
ccopt="-O2"

# Check number of parameters
if [[ "$#" -ne 2 ]] && [[ "$#" -ne 3 ]] && [[ "$#" -ne 4 ]]; then
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
fi

if [[ "$#" == 3 ]]; then
        # Run Spin in verification mode
        echo `$spin -a $promelafile`


        if ! [[ -f "$pan.c" ]]; then
                echo "Error: file $pan.c not generated, exiting."
                exit 1
        fi

        $cc $ccopt -DSAFETY -o $pan $pan.c # FIXME: is DSAFETY appropriate here?

        if ! [[ -x "pan" ]]; then
                echo "Error: executable $pan not generated, exiting."
                exit 1
        fi

        ./$pan > $outputfile 2>&1

        # Clean temporaries relating to verification mode
        rm -f $pan.? $pan
fi

predicate=$3
if [[ "$4" == "verify" ]]; then
        # Run Spin in verification mode
        echo `$spin -f "$predicate" -a $promelafile`


        if ! [[ -f "$pan.c" ]]; then
                echo "Error: file $pan.c not generated, exiting."
                exit 1
        fi

        $cc $ccopt -DSAFETY -o $pan $pan.c # FIXME: is DSAFETY appropriate here?

        if ! [[ -x "pan" ]]; then
                echo "Error: executable $pan not generated, exiting."
                exit 1
        fi

        ./$pan > $outputfile 2>&1

        # Clean temporaries relating to verification mode
        rm -f $pan.? $pan
fi
