#!/bin/bash

# Run Spin in verification mode
# FIXME: extend params to allow selection of specific claims

# Determine path of check script
scriptdir=(`dirname ${BASH_SOURCE[0]}`)
check="$scriptdir/model-check.sh"

# Run check
$check "$@" verify
