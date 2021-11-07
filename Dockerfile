FROM ubuntu:20.04

# This is because the build process was getting stuck
# on the update of tzdata
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America


RUN apt-get update && apt-get install -y \
python3-pip \
libffi-dev \
libnacl-dev \
python3-dev \
ffmpeg
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -U discord.py[voice]
RUN python3 -m pip install --upgrade youtube-dl

WORKDIR /usr/src/bot 
COPY . .

CMD python3 ytchan --token $TOKEN