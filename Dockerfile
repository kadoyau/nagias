# Official Python Docker image
# https://hub.docker.com/_/python
FROM python:3-slim

LABEL maintainer="Yichi Zhang <ichicho@keio.jp>"

WORKDIR /root

# Basic packages and Firefox
RUN apt update && \
    apt install -y --no-install-recommends \
                curl \
                tar \
		firefox-esr && \
    rm -rf /var/lib/apt/lists/*

# Install geckodriver
# https://selenium-python.readthedocs.io/installation.html#drivers
# https://github.com/mozilla/geckodriver/releases
RUN curl -OL https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz && \
    tar -xvzf geckodriver* && \
    mv geckodriver /usr/local/bin && \
    rm geckodriver*

# Install Selenium
RUN pip install --no-cache-dir selenium==4.2.0

WORKDIR /root/nagias

# Default usage: override CMD in *docker run* for proper logintype
CMD ["echo", "Nothing happened. To use nagias, please follow the steps described in README.md."]
