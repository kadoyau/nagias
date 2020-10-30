# Python3 Debian image
FROM python:3
LABEL maintainer="Yichi Zhang <ichicho@keio.jp>"

WORKDIR /root

# Basic packages
RUN apt update && \
    apt install -y --no-install-recommends \
                curl \
                unzip \
                chromium && \
    rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
# https://chromedriver.chromium.org/downloads/version-selection
RUN platform=linux64 && \
    shorten_chrome_version=$(chromium --product-version | sed 's/.[0-9]*$//') && \
    chromedriver_version=$(curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$shorten_chrome_version) && \
    curl -o ./chromedriver.zip http://chromedriver.storage.googleapis.com/$chromedriver_version/chromedriver_$platform.zip && \
    unzip ./chromedriver.zip -d /usr/bin/ && \
    chmod +x /usr/bin/chromedriver

# Install Selenium
RUN pip install --no-cache-dir selenium

# Run nagias
COPY nanaco_auto_fill.py /root
COPY logintype.py /root
# Default usage: override CMD in *docker run* for proper logintype
CMD ["echo", "Nothing happened. To use nagias, please follow the steps described in README.md."]
