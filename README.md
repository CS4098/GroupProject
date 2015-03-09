# GroupProject
[![Build Status](https://travis-ci.org/CS4098/GroupProject.svg?branch=it3)](https://travis-ci.org/CS4098/GroupProject)

Project repo for the CS4098 module in Trinity College Dublin. The purpose of this project is to build a model checker for the PML (process modelling language).


## Development

### Installation With Docker
This project has been developed using a docker image running Ubuntu 12.04. To ensure compatibility with the target machine we recommend using docker for development.

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
* ```cd groupproject && hg clone https://PinPinIre@bitbucket.org/PinPinIre/pml-bnfc```
* ```./launch.sh```
* ```cd /opt/group-project```

## Requirements
### Installation on Ubuntu 12.04
To install natively on Ubuntu 12.04 there are several dependencies that must installed.

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
* ```hg clone https://PinPinIre@bitbucket.org/PinPinIre/pml-bnfc```

## Building
To run the project you need to add ```Pmlxml``` and ```spin``` to your Path. From the checkout location run:
* ```export PATH=$PATH:$PWD/pml-bnfc/xml:$PWD/spin```
If you installed Pmlxml or Spin in another directory you will need to modify the above Path to point to the correct directories.

Build the program:
* ```make build```

Build the program and run unit tests:
* ```make/make test```

Clean target directory:
* ```make clean```

## Running with Web Based UI
The installation process described above should be done before this section. The project should be placed at the top of the Apache document root.

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
### Permissions and PATH
Whatever user Apache is running as needs the permissions to create files in the project directories.

The PATH used by Apache also needs to updated to include spin and the bnfc translator. Apache's original PATH looks like this ```PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin```. We need to update it to include the paths to spin and our pmlxml translator. There are multiple ways of doing this but I chose to add the following line to the envvars file in /etc/apache2/:
* ```export  PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/path/to/pml-bnfc/xml:/path/to/spin```

Apache will then have to be restarted to enable access.

### Testing
To run all of the project test run ```make test``` from the project root directory. 
To test each of the features individually a valid PML file can be uploaded to the apache webserver.
Follow the above instructions to set up the apache server and then visit the location of the projects index.html file.
From there you will be presented with a form where you can upload a pml file. 

There is also the option to select canned predicates.
To use the canned predicates, fill in the required fields and select the checkbox to the side of the predicate.
Click submit to be presented with the output of the program.

The following webpage should contain the inputed pml file, the generated promela code and then the output from running Spin.
So far the following have been implemented and can be tested;
* Processes
* Actions
* Sequence 
* Canned Predicates

