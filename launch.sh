#!/bin/bash
DIR1="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR2="$( cd ../pml-bnfc && pwd )"
docker run -v "$DIR1:/opt/group-project" -v "$DIR2:/opt/pml-bnfc" -t -i cs4098/groupproject /bin/bash
