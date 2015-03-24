# GroupProject
[![Build Status](https://travis-ci.org/CS4098/GroupProject.svg?branch=master)](https://travis-ci.org/CS4098/GroupProject)

Project repo for the CS4098 module in Trinity College Dublin. The purpose of this project is to build a model checker for the PML (process modelling language).


## Requirements
### Installation on Windows
We do not support Windows and cannot guarantee the following will work.

### Installation on Mac OS X
We do not support Mac OS X and cannot guarantee the following will work.

### Installation on Ubuntu 14.04
To install natively on Ubuntu 14.04 there are several dependencies that must installed. Unless otherwise noted, any commands listed here should be run from the project root.

#### Install build tools, curl, mercurial, git, pip, java
* ```sudo apt-get update && sudo apt-get install -y build-essential```
* ```sudo apt-get install -y curl```
* ```sudo apt-get -y install python-pip```
* ```sudo apt-get install -y mercurial```
* ```sudo apt-get install -y git```
* ```sudo apt-get install -y default-jdk```

### Running with Web Based UI

#### HTTP Server
A server is required to run the front end, Apache was used during development and this documentation will be for an Apache set up.
To install the latest version of Apache on Ubuntu use ```sudo apt-get install apache2```

#### Enabling CGI
First, the Apache server must be allowed to execute cgi scripts. Currently the Apache files are located in /etc/apache2, although this may be different in other versions.

Use ```sudo a2enmod cgid``` to enable cgi scripts

#### Project location
Once Apache has been installed, you can download the project files. 
For easiest installation we recommend cloning or copying the project into the apache root directory.
On Ubuntu 14.04 this directory is ```/var/www/html```

When the Project location is chosen Apache needs to be told where cgi scripts will be and what they will look like.

In the /etc/apache2/apache2.conf file add a Directory tag for the project location containing the following directives:
* ```Options +ExecCGI```
* ```AddHandler cgi-script .cgi```

For Example, if the default location is used:
```
<Directory /var/www/>
    Options +ExecCGI
    AddHandler cgi-script .cgi
</Directory>
```

The user Apache runs as will need permissions to create and delete files in the project location. The user can be viewed or changed in the /etc/apache2/envvars file.

#### Python Dependencies
Python 2.6 or later
* ```https://www.python.org/downloads/```

lxml XML parser
* ```sudo apt-get install -y python-lxml```

Other dependencies.
Run this from the project root
* ```pip install -r requirements.txt```

#### Install Spin/Promela
Run either of these from the project root.

64-bit Linux:
* ```mkdir -p spin && curl http://spinroot.com/spin/Bin/spin643_linux64.gz -o spin/spin.gz && gunzip spin/spin.gz && chmod +x spin/spin```

32-bit Linux:
* ```mkdir -p spin && curl http://spinroot.com/spin/Bin/spin643_linux32.gz -o spin/spin.gz && gunzip spin/spin.gz && chmod +x spin/spin```

#### Install Haskell and the BNFC library
* ```sudo apt-get install -y ghc ghc-prof ghc-doc```
* ```sudo apt-get install -y cabal-install```
* ```cabal update```
* ```hg clone https://PinPinIre@bitbucket.org/PinPinIre/pml-bnfc```

### Install Cabal and create sandbox
In order to use a sandboxed environment, cabal version 1.18 or greater is required
* ```cabal install cabal cabal-install```
It has been found that the above can fail due to a missing zlib dependency. If this happens we recommend installing the following.
* ```sudo apt-get install -y zlib1g-dev```

* You may have to update your PATH now as it still points to a version of cabal less than 1.18. Use ```cabal --version``` to check you have the correct version.
* ```cabal sandbox init```
* ```cabal update```

Install haskell dependencies, alex and happy.
* ```sudo apt-get install -y alex```
* ```sudo apt-get install -y happy```
* ```cabal install --only-dependencies```

## Building
To run the project you need to add ```Pmlxml``` and ```spin``` to your Path. From the checkout location run:
* ```export PATH=$PATH:$PWD/.cabal-sandbox/bin:$PWD/spin```
If you installed Spin or the cabal sandbox in another directory you will need to modify the above Path to point to the correct directory.

Build the program:
* ```make build```

Build the program and run unit tests:
* ```make test```

Clean target directory:
* ```make clean```

### Apache PATH

The PATH used by Apache also needs to updated to include spin and the bnfc translator. Apache's original PATH looks like this ```PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin```. 

We need to update it to include the paths to spin and our pmlxml translator (Which should be installed into the cabal sandbox).
Add the following line to /etc/apache2/envvars (replacing <path-to-project> with the path to where the project is located e.g. /var/www/html/GroupProject):
* ```export  PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:<path-to-project>/pml-bnfc/xml:<path-to-project>/spin```

Apache will then have to be restarted to enable access ```sudo /etc/init.d/apache2 restart```.

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
* Process
* Action
* Sequence
* Selection
* Branch
* User-space predicates

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
### Selection
To test selection, pass a pml file containing selection constructs to the system.

Example selection construct:
```
process test {
    selection {
        action act1 {
	        requires { a }
	        provides { a }
        }
        sequence one {
		    action act2 {
		        requires { a }
                provides { c }
		    }
            action act3 {
		        requires { c }
                provides { b }
		    }
	    }
    }
}
```

When run, the system will perform either Action act1 or Sequence one, which consists of act2 and act3.

### Branch
To test branch, pass a pml file containing branch constructs to the system.

Example branch construct:
```
process test{
	branch br1 {
		sequence seq1 {
			action act_1 {
			requires { a }
			provides { b }
			}
			action act_2 {
			requires { b }
			provides { c }
			}
		}
		sequence seq2 {
			action act_3 {
			requires { d }
			provides { e }
			}
			action act_4 {
			requires { e }
			provides { f }
			}
		}
	}
}
```
When run, the system will perform Sequences seq1 and seq2 in parallel.

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

There are additional dependencies when installing with Docker:

* Git: ```sudo apt-get install -y git```
* Mercurial: ```sudo apt-get install -y mercurial```

After Docker has been installed:

* ```docker pull cs4098/groupproject```
* ```git clone https://github.com/cs4098/groupproject```
* ```cd groupproject && hg clone https://PinPinIre@bitbucket.org/PinPinIre/pml-bnfc```
* ```./launch.sh```
* ```cd /opt/group-project```

