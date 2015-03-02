#!/bin/bash

# Run Spin in test mode (single path of execution)

# Determine path of check script
scriptdir=(`dirname ${BASH_SOURCE[0]}`)
check="$scriptdir/model-check.sh"

# Run check
$check "$@"
