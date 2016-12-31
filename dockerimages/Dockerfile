# in ubuntu 16.04, install python-3.6, g++
FROM ubuntu:16.04
RUN apt-get update

# settings for install
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

# install python-3.6
RUN apt-get install -y python3.6

# install g++ latest
RUN apt-get install -y g++

# clear apt cache
RUN rm -rf /var/lib/apt/lists/*
