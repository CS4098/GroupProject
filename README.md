# GroupProject
Project repo for the CS4098 module in Trinity College Dublin

## Requirements

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

##### Ubuntu 12.04 Without Docker
If you wish to install natively on Ubuntu 12.04 without Docker there are several dependencies that must installed.

* ```apt-get update && apt-get install -y build-essential```
* ```apt-get install -y curl```
* ```apt-get install mercurial```
* ```apt-get install -y git```
* ```apt-get update && apt-get install -y openjdk-7-jdk```
* ```apt-get update && apt-cache search maven && apt-get install -y maven```
* ```update-alternatives --set java /usr/lib/jvm/java-7-openjdk-amd64/jre/bin/java```
* ```curl http://spinroot.com/spin/Bin/spin643_linux64.gz -o /bin/spin.gz && gunzip /bin/spin.gz && chmod +x /bin/spin```
* ```mkdir -p /usr/local/java/JLex && mkdir -p /usr/local/java/Cup```
* ```curl http://www.cs.princeton.edu/~appel/modern/java/CUP/java_cup_v10k.tar.gz -o /usr/local/java/Cup/Cup.tar.gz && tar -zxvf /usr/local/java/Cup/Cup.tar.gz -C /usr/local/java/Cup/ && rm /usr/local/java/Cup/Cup.tar.gz```
* ```mkdir -p /usr/local/java/JLex && curl http://www.cs.princeton.edu/~appel/modern/java/JLex/current/Main.java -o /usr/local/java/JLex/Main.java && javac -Xlint /usr/local/java/JLex/Main.java```
* ```cd /opt/ && hg clone https://PinPinIre@bitbucket.org/PinPinIre/pml-bnfc && git clone https://github.com/cs4098/groupproject```
* ```echo 'export CLASSPATH=$CLASSPATH:/opt/pml-bnfc/java1.5:/usr/local/java/Cup:/usr/local/java' >> ~/.bashrc```

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
