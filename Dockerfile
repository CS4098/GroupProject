FROM ubuntu:12.04
MAINTAINER Cathal Geoghegan <geogheca@tcd.ie>
RUN apt-get update && apt-get install -y build-essential
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get install -y mercurial
RUN curl http://spinroot.com/spin/Bin/spin643_linux64.gz -o /bin/spin.gz && gunzip /bin/spin.gz && chmod +x /bin/spin
RUN apt-get install -y haskell-platform && cabal update
RUN cd /opt/ && hg clone https://PinPinIre@bitbucket.org/PinPinIre/pml-bnfc && cd pml-bnfc/xml && make