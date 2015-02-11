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

=======
##### Ubuntu 12.04 Without Docker
If you wish to install natively on Ubuntu 12.04 without Docker there are several dependencies that must installed.

Install build tools, curl, mercurial, git, Java and set correct Java version
* ```apt-get update && apt-get install -y build-essential```
* ```apt-get install -y curl```
* ```apt-get install mercurial```
* ```apt-get install -y git```
* ```apt-get update && apt-get install -y openjdk-7-jdk```
* ```update-alternatives --set java /usr/lib/jvm/java-7-openjdk-amd64/jre/bin/java```

Install Maven, Gradle, Spin/Promela, 
* ```apt-get update && apt-cache search maven && apt-get install -y maven```
* ```apt-get install -y software-properties-common python-software-properties&& add-apt-repository -y ppa:cwchien/gradle && apt-get update && apt-get install -y gradle```
* ```curl http://spinroot.com/spin/Bin/spin643_linux64.gz -o /bin/spin.gz && gunzip /bin/spin.gz && chmod +x /bin/spin```

Install Haskell platform and the BNFC library
* ```apt-get install -y haskell-platform && cabal update```
* ```cd /opt/ && git clone https://github.com/BNFC/bnfc && cd bnfc/source && cabal install```

Install Java dependencies for the files generated by BNFC program and get repos
* ```mkdir -p /usr/local/java/JLex && mkdir -p /usr/local/java/Cup```
* ```curl http://www.cs.princeton.edu/~appel/modern/java/CUP/java_cup_v10k.tar.gz -o /usr/local/java/Cup/Cup.tar.gz && tar -zxvf /usr/local/java/Cup/Cup.tar.gz -C /usr/local/java/Cup/ && rm /usr/local/java/Cup/Cup.tar.gz```
* ```mkdir -p /usr/local/java/JLex && curl http://www.cs.princeton.edu/~appel/modern/java/JLex/current/Main.java -o /usr/local/java/JLex/Main.java && javac -Xlint /usr/local/java/JLex/Main.java```
* ```cd /opt/ && hg clone https://PinPinIre@bitbucket.org/PinPinIre/pml-bnfc && git clone https://github.com/cs4098/groupproject```

Update Classpath and add cabal to Path
* ```echo 'export CLASSPATH=$CLASSPATH:/opt/pml-bnfc/java1.5:/usr/local/java/Cup:/usr/local/java' >> ~/.bashrc```
* ```echo 'export PATH="$HOME/.cabal/bin:$PATH"' >> ~/.bashrc```

Compile BNCF java files
* ```cd /opt/pml-bnfc/java1.5 && bnfc -m -java ../PML.cf && make```


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
