FROM python:3

WORKDIR /root

RUN apt update && \
    apt install -y --no-install-recommends \
                curl \
                unzip && \
    rm -rf /var/lib/apt/lists/*

RUN curl -o ./chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt update && \
    apt install -y --no-install-recommends --fix-broken \
                ./chrome.deb && \
    rm -rf /var/lib/apt/lists/*

RUN PLATFORM=linux64 && \
    SHORTEN_CHROME_VERSION=$(google-chrome --version | sed 's/[^0-9.]*//g' | sed 's/.[0-9]*$//') && \
    CHROMEDRIVER_VERSION=$(curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$SHORTEN_CHROME_VERSION) && \
    curl -o ./chromedriver.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_$PLATFORM.zip && \
    unzip ./chromedriver.zip -d /usr/bin/ && \
    chmod +x /usr/bin/chromedriver

RUN pip install --no-cache-dir selenium

CMD chromedriver
