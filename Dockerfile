# Pull base image.
FROM ubuntu:18.04

# Install.
RUN \
  apt-get update && \
  apt-get install -y python3 && \
  apt-get install -y git python3-pip default-jdk && \
  git clone --recursive https://github.com/alessandrodd/apk_api_key_extractor.git && \
  cd apk_api_key_extractor && \
  cp config.example.yml config.yml && \
  pip3 install -r requirements.txt 

# Add files.
COPY apks /apk_api_key_extractor/apks/

# Set environment variables.
ENV HOME /
ENV PATH /usr/bin:$PATH

# Set workdir
WORKDIR /apk_api_key_extractor

# Define default command.
CMD python3 /apk_api_key_extractor/main.py --monitor-apks-folder

