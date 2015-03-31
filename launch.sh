#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
docker run -p 8080:80 -v "$DIR:/opt/group-project" -t -i cs4098/groupproject /bin/bash 
