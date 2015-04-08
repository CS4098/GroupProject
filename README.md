# GroupProject
[![Build Status](https://travis-ci.org/CS4098/GroupProject.svg?branch=master)](https://travis-ci.org/CS4098/GroupProject)

Project repo for the CS4098 module in Trinity College Dublin. The purpose of this project is to build a model checker for the PML (process modelling language).


# Requirements
## Installation on Windows
We do not support Windows and cannot guarantee the following will work.

## Installation on Mac OS X
We do not support Mac OS X and cannot guarantee the following will work.

## Installation on Ubuntu 14.04
To install natively on Ubuntu 14.04 there are several dependencies that must installed.

### Install build tools, curl, mercurial, git, pip, java
* ```sudo apt-get update && sudo apt-get install -y build-essential```
* ```sudo apt-get install -y curl```
* ```sudo apt-get install -y python-pip```
* ```sudo apt-get install -y mercurial```
* ```sudo apt-get install -y git```
* ```sudo apt-get install -y default-jdk```

### Install and Setup Apache

#### HTTP Server
A server is required to run the front end, Apache was used during development and this documentation will be for an Apache set up.
To install the latest version of Apache on Ubuntu use ```sudo apt-get install -y apache2```

#### Enabling CGI
First, the Apache server must be allowed to execute cgi scripts. Currently the Apache files are located in /etc/apache2, although this may be different in other versions.

Use ```sudo a2enmod cgid``` to enable cgi scripts

After enabling CGI, Apache must be restarted, however this can wait for the moment as we are about to edit the config file.

### Project location
Once Apache has been installed, you can download the project files. 
For easiest installation we recommend cloning or copying the project into the apache root directory.
On Ubuntu 14.04 this directory is ```/var/www/html```. To clone the project to this location use:
* ```cd /var/www/html```
* ```sudo git clone https://github.com/CS4098/GroupProject```
* ```cd GroupProject```

Unless otherwise noted, any commands listed here from now on should be run from the project root.

When the Project location is chosen Apache needs to be told where cgi scripts will be and what they will look like. Open the apache2.conf file:
* ```sudo emacs /etc/apache2/apache2.conf```

In the /etc/apache2/apache2.conf file add a Directory tag for the project location containing the following directives:
* ```Options +ExecCGI```
* ```AddHandler cgi-script .cgi```

For Example, if the default location is used:
```
<Directory /var/www/html/>
    Options +ExecCGI
    AddHandler cgi-script .cgi
</Directory>
```

Now Apache must be restarted so all changes take effect.
* ```sudo service apache2 restart```

### Python Dependencies
Python 2.6 or later
* ```https://www.python.org/downloads/```

lxml XML parser
* ```sudo apt-get install -y python-lxml```

Other dependencies.
Run this from the project root
* ```sudo pip install -r requirements.txt```

### Install Spin/Promela
Run this from the project root.

64-bit Linux:
* ```sudo mkdir -p spin && sudo curl http://spinroot.com/spin/Bin/spin643_linux64.gz -o spin/spin.gz && sudo gunzip spin/spin.gz && sudo chmod +x spin/spin```

### Install Haskell and the BNFC library
* ```sudo apt-get install -y ghc ghc-prof ghc-doc```
* ```sudo apt-get install -y cabal-install```
* ```cabal update```
* ```sudo hg clone https://PinPinIre@bitbucket.org/PinPinIre/pml-bnfc```

### Apache Permissions

The user Apache runs as will need permissions to create and delete files in the project location. The user can be viewed or changed in the /etc/apache2/envvars file. The default Apache user is ```www-data```; if you change this user, wherever ```www-data``` is seen in the following commands, you will need to replace it with your given user name. To give this user the appropriate permissions, run:
* ```sudo chown -R www-data:www-data /var/www/html/GroupProject```

Now this will cause some permissions issues with the Ubuntu user you are personally using. We suggest using groups to solve this as detailed here. This will involve having to log out and log back in. We have provided alternate solutions (if you don't want to follow this method or if it does not work for you) in a section titled "Alternative Apache Permissions" further below in this document.

To add the current user to the www-data group and give the group write permissions in the project directory use the following commands (replacing "username" with your own username):
* ```sudo usermod -a -G www-data username```
* ```sudo chmod -R g+w /var/www/html/GroupProject```

You MUST log out and log back in now for these changes to take effect.

### Install Cabal and create sandbox

In order to use a sandboxed environment, cabal version 1.18 or greater is required.
It has been found that the installation can fail due to a missing zlib dependency so we recommend installing zlib first:
* ```sudo apt-get install -y zlib1g-dev```
* ```cabal install cabal cabal-install```

You may have to update your PATH now as it still points to a version of cabal less than 1.18. By default, cabal will install to the current user's home directory. To modify PATH run:
* ```export PATH=~/.cabal/bin:$PATH```

Use ```cabal --version``` to check you have the correct version. From the project root run:

* ```cabal sandbox init```
* ```cabal update```

Install haskell dependencies, alex and happy.
* ```sudo apt-get install -y alex```
* ```sudo apt-get install -y happy```
* ```cabal install --only-dependencies```

### Apache PATH

The PATH used by Apache also needs to updated to include spin and the bnfc translator. Apache's original PATH looks like this ```PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin```. 

We need to update it to include the paths to spin and our pmlxml translator (Which should be installed into the cabal sandbox). Open the envvars file:
* ```sudo emacs /etc/apache2/envvars```

Add the following line (replacing ```<path-to-project>``` with the path to where the project is located e.g. /var/www/html/GroupProject):
* ```export  PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:<path-to-project>/.cabal-sandbox/bin:<path-to-project>/spin```

Apache will then have to be restarted to enable access:
* ```sudo service apache2 restart```.

### Building
To run the project you need to add ```Pmlxml``` and ```spin``` to your Path. From the checkout location run:
* ```export PATH=$PATH:$PWD/.cabal-sandbox/bin:$PWD/spin```

If you installed Spin or the cabal sandbox in another directory you will need to modify the above Path to point to the correct directory.

Build the program:
* ```make build```

Build the program and run unit tests:
* ```make test```

Clean target directory:
* ```make clean```

## Running with Web Based UI

### Using the UI

Apache uses 127.0.0.1 as the default local IP address. Navigating to http://127.0.0.1/GroupProject in any web browser should take you to the web page.

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

## Alternative Apache Permissions

### Running commands as www-data

Instead of adding the current user to the www-data group we can run commands as the www-data user. We still change ownership of the project to www-data using ```sudo chown -R www-data:www-data /var/www/html/GroupProject```. However instead of adding the current user to the group we modify some of the commands:
*```cabal sandbox init``` -> ```sudo env PATH=$PATH' cabal sandbox init```
*```make build``` -> ```sudo -u www-data env PATH=$PATH' make build```
*```make test``` -> ```sudo -u www-data env PATH=$PATH' make test```
*```make clean``` -> ```sudo -u www-data env PATH=$PATH' make clean```

### Changing Apache's default user
Instead of changing ownership of the project directory to www-data change it to be the current user (replacing "username" with your own username):
*```sudo chown -R username:username /var/www/html/GroupProject```

In the /etc/apache2/envvars file we can change the user and group that Apache runs as. This means we can set it to be the current user.
Use ```sudo emacs /etc/apache2/envvars``` and change the following lines (replacing "username" with your own username):
* ```export APACHE_RUN_USER=www-data``` -> ```export APACHE_RUN_USER=username```
* ```export APACHE_RUN_GROUP=www-data``` -> ```export APACHE_RUN_GROUP=username```

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

Note that, due to a restriction concerning the underlying Spin system, nested branching is not supported. Entering a PML file featuring nested branch constructs produces undefined behaviour.

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

