FROM ubuntu:12.04
MAINTAINER Cathal Geoghegan <geogheca@tcd.ie>
RUN apt-get update && apt-get install -y build-essential
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get update && apt-get install -y openjdk-7-jdk
RUN apt-get update && apt-cache search maven && apt-get install -y maven
RUN update-alternatives --set java /usr/lib/jvm/java-7-openjdk-amd64/jre/bin/java
RUN curl http://spinroot.com/spin/Bin/spin643_linux64.gz -o /bin/spin.gz && gunzip /bin/spin.gz && chmod +x /bin/spin
RUN mkdir -p /usr/local/java/JLex && mkdir -p /usr/local/java/Cup
RUN curl http://www.cs.princeton.edu/~appel/modern/java/CUP/java_cup_v10k.tar.gz -o /usr/local/java/Cup/Cup.tar.gz && tar -zxvf /usr/local/java/Cup/Cup.tar.gz -C /usr/local/java/Cup/ && rm /usr/local/java/Cup/Cup.tar.gz
RUN mkdir -p /usr/local/java/JLex && curl http://www.cs.princeton.edu/~appel/modern/java/JLex/current/Main.java -o /usr/local/java/JLex/Main.java && javac -Xlint /usr/local/java/JLex/Main.java
RUN echo 'export CLASSPATH=/opt/pml-bnfc/java1.5:/usr/local/java/Cup:/usr/local/java' >> ~/.bashrc