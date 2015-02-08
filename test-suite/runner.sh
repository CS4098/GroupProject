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

# Set up logging
ts=(`date "+%F-%H-%M-%S"`)
logfile="$ts.log"
touch $logfile

# Set up counts
count_total=0
count_failed=0

# Process input tests
for dir in $2/*/
do
	echo "[--- $dir ---]" >> $logfile
	for filepath in $dir/*.pml
	do
		pml_filename=(`basename $filepath`)
		echo -e "\tTest found: $pml_filename" >> $logfile

		basename="${pml_filename%.*}"

		expected_filepath="$dir$basename.pml.expected"
		if ! [[ -f  $expected_filepath ]]; then
			echo -e "\tError: expected promela file not found, skipping." >> $logfile
			continue
		fi
		expected_filename=(`basename $expected_filepath`)
		echo -e "\tExpected promela file found: $expected_filename" >> $logfile
		count_total=$((count_total+1))

		echo >> $logfile
	done
done

# Print summary to file and console
count_succeeded=$(($count_total-$count_failed))
summary="[=== SUMMARY ===]\n\tTOTAL: $count_total\n\tFAILED: $count_failed\n\tSUCCEEDED: $count_succeeded"
echo -e $summary >> $logfile
echo -e $summary
echo -e "\nLog available at: $logfile"
