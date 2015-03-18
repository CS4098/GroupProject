# GroupProject
[![Build Status](https://travis-ci.org/CS4098/GroupProject.svg?branch=master)](https://travis-ci.org/CS4098/GroupProject)

Project repo for the CS4098 module in Trinity College Dublin. The purpose of this project is to build a model checker for the PML (process modelling language).


## Requirements
### Installation on Windows
We do not support Windows and cannot guarantee the following will work.

### Installation on Mac OS X
We do not support Mac OS X and cannot guarantee the following will work.

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

### Install Cabal and create sandbox
In order to use a sandboxed environment, cabal version 1.18 or greater is required
* ```cabal install cabal cabal-install```
* You may have to update your PATH now as it still points to a version of cabal less than 1.18. Use ```cabal --version``` to check you have the correct version.
* ```cabal sandbox init```
* ```cabal update```

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
* ```export  PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/path/to/pml-bnfc/xml:/path/to/spin:$PATH```

Apache will then have to be restarted to enable access.

## Running from Command-Line

PML files are internally translated into Promela code. Promela is the language used by Spin, a model-checker. The configuration provided here returns the output from Spin, and also makes available the intermediate Promela representation.

To be able to run commands easily, first adjust ```PATH``` from the checkout location:
* ```export PATH=$PATH:$PWD/src/main/translator-xml:$PWD/src/main/model-checker```

### Translating PML to Promela

```PMLToPromela.sh <path-to-input-PML-file> <path-to-output-Promela-file> <path-to-predicate-file>```

where
* ```<path-to-input-PML-file>``` is the input PML file.
* ```<path-to-output-Promela-file>``` is the desired target Promela file; if file already exists, the script will over-write it.
* ```<path-to-predicate-file>``` is the predicate file.

### Running the model-checker

```model-check.sh <path-to-input-Promela-file> <path-to-Spin-output-file> [verify]```

where
* ```<path-to-input-Promela-file>``` is the input Promela file.
* ```<path-to-Spin-output-file>``` is the target file where Spin output is to be redirected to; if the file already exists, the script will over-write it.
* ```[verify]``` specifies that Spin is to be run in Verification mode. By default, Spin is run in Test mode, where only a single possible path of execution is run. Running Spin in Verification mode allows the testing of claims against all possible program states.

#### Replaying Trail Files

When Spin is run in Verification mode, and either times out or finds a counter-example, a trail file will be generated. The trail file may be replayed in Spin to show all steps leading up to the timeout or assertion failure. The output from replaying it may be viewed as follows:

```replay-trail.sh <path-to-promela-file> <path-to-trail-file> <path-to-spin-output-file>```

where
* ```<path-to-promela-file>``` is the original input Promela file.
* ```<path-to-trail-file>``` is the trail file; its location will be given in the Spin output from when it was run in Verification mode.
* ```<path-to-spin-output-file>``` is the target file where Spin output is to be redirected to; if the file already exists, the script will over-write it.

## Testing
To run all of the project test run ```make test``` from the project root directory. 
To test each of the features individually a valid PML file can be uploaded to the apache webserver.
Follow the above instructions to set up the apache server and then visit the location of the projects index.html file.
From there you will be presented with a form where you can upload a pml file. 
Click submit to be presented with the output of the program.

The following webpage should contain the inputed pml file and at the generated promela code.
At the bottom of this page there is radio selection where you can select the start state for each resource.
Leave these in their default state to test the pml constructs.
These resources can be changed and constitute the "User-space to predicate" feature.

The following webpage displays the run promela code and the the output from running Spin.
So far the following have been implemented and can be tested;
* Processes
* Actions
* Sequence 
* Canned Predicates
* User-space to predicate

The entire web interface constitutes the plumbing feature.
There are selenium tests which test the plumbing functionality.

### Process
To test process an empty pml process can be passed to the model checker

Empty Process:
```
process test {
}
```
Produces spin output in which all states are reached. This verifies that all states in the pml process can be reached.

### Actions

Unreachable action:
```
process test_action {
    action act {
	requires { a }
	provides { a }
    }
}
```
Produces spin output in which there is an invalid end state. As the "act" action requires "a" and "a" is never provided by any other action the "act" action cannot be completed.

All actions reachable:
```
process abc {
    action a {
	provides { b }
    }
    action b {
	requires { b }
	provides { c }
    }
    action c {
	requires { c }
	provides { d }
    }
}
```
Produces spin output in which all states are reached.

Some actions reachable and some not:
```
process abc {
    action a {
	provides { b }
    }
    action b {
	requires { b }
	provides { c }
    }
    action c {
	requires { a }
	provides { d }
    }
}
```
Produces spin output which has failed as action c is unreachable in the the pml file.

### Sequence
To test sequences a pml file containing sequence constructs is passed to the system.

Basic sequence without any actions
```
process test {
	sequence one {
	}
}
```
The above passes as all states can be reached. There are also no resources and thus the User Space feature cannot be used here.

Sequence with an action which cannot proceed
```
process test {
	sequence one {
		action act {
		requires { a }
		provides { b }
		}
	}
}
```
The above fails as a is never provided.

Sequence which completes as all actions can proceed
```
process abc {
	sequence one {
		action a {
		provides { b }
		}
		action b {
		requires { b }
		provides { c }
		}
		action c {
		requires { c }
		provides { d }
		}
	}
}
```


### User Space Predicates
The user space feature can be tested on the second webpage in the radio select boxes at the bottom of the page.
The radio buttons allow the user to specify the start state of each resource in the PML system. 
By default each resource is left as false. 
By changing to true this allows the resource to be provided as soon as the system starts.


## Development

### Installation With Docker
This project has been developed using a docker image running Ubuntu 12.04. To ensure compatibility with the target machine, docker can be used for development. We do not recommend using docker for anything other than development.

#### Mac OSX

See: [Boot2Docker](https://github.com/boot2docker/boot2docker)

#### Linux (64-bit)

##### Debian
See: [https://docs.docker.com/installation/debian/](https://docs.docker.com/installation/debian/)

##### Ubuntu
See: [http://docs.docker.com/installation/ubuntulinux/](http://docs.docker.com/installation/ubuntulinux/)

There are additional dependencies when installing with Docker. The following must be installed with superuser privileges:

* Git: ```apt-get install -y git```
* Mercurial: ```apt-get install -y mercurial```

After Docker has been installed:

* ```docker pull cs4098/groupproject```
* ```git clone https://github.com/cs4098/groupproject```
* ```cd groupproject && hg clone https://PinPinIre@bitbucket.org/PinPinIre/pml-bnfc```
* ```./launch.sh```
* ```cd /opt/group-project```

