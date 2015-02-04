FROM ubuntu:12.04
MAINTAINER Cathal Geoghegan <geogheca@tcd.ie>
RUN apt-get update && apt-get install -y build-essential
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get update && apt-get install -y openjdk-7-jdk
RUN apt-get update && apt-cache search maven && apt-get install -y maven
RUN update-alternatives --set java /usr/lib/jvm/java-7-openjdk-amd64/jre/bin/java
