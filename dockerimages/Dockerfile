# in ubuntu 16.04, install python-3.6, g++
FROM ubuntu:16.04
RUN apt-get update

# settings for install
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt update

# install python-3.6
RUN apt install -y python3.6

# install g++ latest
RUN apt install -y g++

# install git latest
RUN apt install -y git

# install make
RUN apt install -y make

# make working directory and change current directory
RUN mkdir /workdir

# install judge client and set up
RUN cd /workdir && git clone https://github.com/AJudge-team/Judge.git
RUN cd /workdir/Judge && make
RUN mv /workdir/Judge/Judge /workdir/judge_client
RUN rm -rf /workdir/Judge/

# remove git
RUN apt autoremove git

# remove make
RUN apt autoremove make

# clear apt cache
RUN rm -rf /var/lib/apt/lists/*
