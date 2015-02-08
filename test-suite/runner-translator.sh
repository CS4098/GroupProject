#!/bin/bash

usage="Usage: runner <path-to-binary> <path-to-input-test-dir>"

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

transdir=(`dirname $translator`) # Directory where temporary artefacts to be placed

# Check the second parameter is the path to a directory
suite=$2
if ! [[ -d $suite ]]; then
	echo "$usage: given path to input tests is not a directory."
	exit 1
fi

# Set up logging
ts=(`date "+%F-%H-%M-%S"`)
logdir="$transdir/logs-translator"
mkdir -p $logdir
logfile="$logdir/$ts.log"
touch $logfile

echo "-------------------------------------------------------"
echo " PML-TO-PROMELA TRANSLATOR TESTS"
echo "-------------------------------------------------------"

# Set up counts
count_total=0
count_failed=0

# Process input tests
for dir in $2/*/
do
	echo -e "[--- $dir ---]" >> $logfile
	for filepath in $dir/*.pml
	do
		# Get all necessary file paths
		pml_filename=(`basename $filepath`)
		echo -e "PML file found: $pml_filename" >> $logfile

		basename="${pml_filename%.*}"

		expected_filepath="$dir$basename.pml.expected"
		if ! [[ -f  $expected_filepath ]]; then
			echo -e "Error: expected promela file \"$expected_filepath\" not found, skipping." >> $logfile
			continue
		fi
		expected_filename=(`basename $expected_filepath`)
		echo -e "Expected promela file found: $expected_filename" >> $logfile
		count_total=$((count_total+1))

		actual_filename="$transdir/$basename.pml.actual"

		# Run program (convert PML to promela)
		com="./$translator $pml_filename $actual_filename"
		echo -e "Running test: $basename... " >> $logfile
		echo -n "Running test: $basename... "
		echo -e "-------" >> $logfile
		$com >> $logfile
		echo -e "-------" >> $logfile

		# Translator fails to create promela file
		if [[ ! -f $actual_filename ]]; then
			echo -e "Error: no promela file created"
			count_failed=$((count_failed+1))
			echo "FAIL" >> $logfile
			echo "FAIL"
			continue
		fi

		# Compare output
		result=(`diff -q $expected_filepath $actual_filename`)
		if [[ "$result" != "" ]]; then
			echo -e "*** Expected and actual promela files differ ***" >> $logfile
			count_failed=$((count_failed+1))
			echo "FAIL" >> $logfile
			echo "FAIL"
		else
			echo "PASS" >> $logfile
			echo "PASS"
		fi

		# Clean up artefacts
		if [[ -f $actual_filename ]]; then
			rm $actual_filename
		fi

		echo >> $logfile
	done
done

# Print summary to file and console
count_succeeded=$(($count_total-$count_failed))
summary="\nRESULTS: Total: $count_total, Failures: $count_failed"
echo -e $summary >> $logfile
echo -e $summary
echo -e "Log available at: $logfile\n"
