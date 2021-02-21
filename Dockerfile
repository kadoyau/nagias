# Official Python Docker image
# https://hub.docker.com/_/python
FROM python:3-alpine
LABEL maintainer="Yichi Zhang <ichicho@keio.jp>"

# Non-root user name
ARG user=nagias

# Install Chromium, ChromeDriver, Selenium
RUN apk add --no-cache \
            curl \
            chromium \
            chromium-chromedriver && \
    pip install --no-cache-dir selenium

# Add non-root user
ARG home=/home/$user
RUN addgroup -S $user && \
    adduser -S $user -G $user
USER $user
WORKDIR $home

# Copy necessary project files
COPY nanaco_auto_fill.py $home
COPY logintype.py $home

# Default usage: override CMD in *docker run* for proper logintype
CMD ["echo", "Nothing happened. To use nagias, please follow the steps described in README.md."]
