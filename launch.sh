#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
docker run -v "$DIR:/opt/group-project" -t -i cs4098/groupproject /bin/bash
