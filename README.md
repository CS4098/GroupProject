# GroupProject
[![Build Status](https://travis-ci.org/CS4098/GroupProject.svg?branch=it2)](https://travis-ci.org/CS4098/GroupProject)
Project repo for the CS4098 module in Trinity College Dublin

## Requirements

### Installation With Docker

#### Mac OSX

See: [Boot2Docker](https://github.com/boot2docker/boot2docker)

#### Linux (64-bit)

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

=======
### Installation on Ubuntu 12.04 Without Docker
If you wish to install natively on Ubuntu 12.04 without Docker there are several dependencies that must installed.

#### Install build tools, curl, mercurial, git
* ```apt-get update && apt-get install -y build-essential```
* ```apt-get install -y curl```
* ```apt-get install mercurial```
* ```apt-get install -y git```

#### Python Dependencies
Python 2.6 or later
* ```https://www.python.org/downloads/```

lxml XML parser
* ```apt-get install python-lxml```

Other dependencies
* ```pip install -r requirements.txt```

#### Install Spin/Promela
64-bit Linux:
* ```mkdir -p spin && curl http://spinroot.com/spin/Bin/spin643_linux64.gz -o spin/spin.gz && gunzip spin/spin.gz && chmod +x spin/spin```

32-bit Linux:
* ```mkdir -p spin && curl http://spinroot.com/spin/Bin/spin643_linux32.gz -o spin/spin.gz && gunzip spin/spin.gz && chmod +x spin/spin```

#### Install Haskell platform and the BNFC library
* ```apt-get install -y haskell-platform && cabal update```

#### Compile BNCF XML generator. From the checkout location run:
* ```cd pml-bnfc/xml && make```


## Building
Build the program:
* ```make build```

To run the project you need to add ```Pmlxml``` and ```spin``` to your Path. From the checkout location run:
* ```export PATH=$PATH:$PWD/pml-bnfc/xml:$PWD/spin```

Build the program and run unit tests:
* ```make/make test```

Build the program and install to destination:
* ```export DESTDIR=<path-to-destination>```
* ```make install```

Clean target directory:
* ```make clean```

## Running with Web Based UI

### HTTP Server
A server is required to run the front end, Apache was used during development and this documentation will be for an Apache set up.
To install the latest version of Apache on Ubuntu use ```sudo apt-get install apache2```

### Enabling CGI
First, the Apache server must be allowed to execute cgi scripts. Currently the Apache files are located in /etc/apache2, although this may be different in other versions.
Make sure that the mods-enabled directory contains ```cgid.conf``` and ```cgid.load```
If not, create a symbolic link to their locations in the mods-available directory:
* ```ln -s /etc/apache2/mods-available/cgid.conf /etc/apache2/mods-enabled/```
* ```ln -s /etc/apache2/mods-available/cgid.load /etc/apache2/mods-enabled/```

Next, Apache must be told where cgi scripts will be and what they will look like, there are a number of ways of doing this which can be found here: http://httpd.apache.org/docs/2.2/howto/cgi.html
I used the following method:
Edit the appropriate file in the sites-enabled folder (such as 000-default), so that after the document root is declared we tell Apache that files ending with .cgi are cgi scripts (/var/www/ may need to be changed if this is not your document root):
```
<Directory /var/www/>
    Options +ExecCGI
    AddHandler cgi-script .cgi
</Directory>
```
### Moving and changing index.html
The project folder should be placed below the Apache document root.
The web app files can be found in src/main/webapp/
The index.html can be moved to (or symlinked from) the project root directory for url convenience.
The index.html file should also be checked so that the form action correctly points to the location of the python.cgi script.

The web app can then be used by going to http://{serverIP}/GroupProject/src/main/webapp/
This url will change if the project is not put at the top of the document root or if directories are renamed or files are moved.
e.g. http://127.0.0.1/GroupProject/ (if the index.html is moved to the project root directory)


