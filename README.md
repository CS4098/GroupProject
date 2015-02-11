# GroupProject
Project repo for the CS4098 module in Trinity College Dublin

## Requirements

### Docker

#### Mac OSX

See: [Boot2Docker](https://github.com/boot2docker/boot2docker)

#### Linux

##### Debian
See: [https://docs.docker.com/installation/debian/](https://docs.docker.com/installation/debian/)

##### Ubuntu
See: [http://docs.docker.com/installation/ubuntulinux/](http://docs.docker.com/installation/ubuntulinux/)

After Docker has been installed:

* ```docker pull cs4098/groupproject```
* ```git clone https://github.com/cs4098/groupproject```
* ```hg clone https://PinPinIre@bitbucket.org/PinPinIre/pml-bnfc```
* ```cd groupproject && ./launch.sh```
* ```cd /opt/group-project```

### Http Server
Currently the html file can be tested "locally" by changing the action in the form from "python.cgi" to "http://dar.netsoc.ie/group/python.cgi"

To run on an apache server, make sure the config allows for cgi scripts http://httpd.apache.org/docs/2.2/howto/cgi.html
If the python.cgi file is moved to a cgi-bin directory, change the action in the html form appropriately

## Building

Build the program:
* ```make build```

Build the program and run unit tests:
* ```make/make test```

Build the program and install to destination:
* ```export DESTDIR=<path-to-destination>```
* ```make install```

Clean target directory:
* ```make clean```
