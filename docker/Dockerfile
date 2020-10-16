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

RUN platform=linux64 && \
    shorten_chrome_version=$(google-chrome --version | sed 's/[^0-9.]*//g' | sed 's/.[0-9]*$//') && \
    chromedriver_version=$(curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$shorten_chrome_version) && \
    curl -o ./chromedriver.zip http://chromedriver.storage.googleapis.com/$chromedriver_version/chromedriver_$platform.zip && \
    unzip ./chromedriver.zip -d /usr/bin/ && \
    chmod +x /usr/bin/chromedriver

RUN pip install --no-cache-dir selenium

CMD chromedriver
