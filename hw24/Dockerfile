FROM python:3

#Copy test project files to the image folder
RUN git clone --progress --verbose https://github.com/victorinausk/otus_qa.git ./app

#Make the folder as a working directory
WORKDIR /app

#Install the test project libraries
RUN pip install nose pylint
RUN pip install browsermob-proxy
RUN pip install -r requirements.txt
RUN apt-get install -yqq unzip
RUN apt-get install curl

# Chromedriver

ENV CHROMEDRIVER_DIR /app
RUN wget -O /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver_linux64.zip -d /app

# Chrome
RUN curl https://dl-ssl.google.com/linux/linux_signing_key.pub -o /tmp/google.pub \
    && cat /tmp/google.pub | apt-key add -; rm /tmp/google.pub \
    && echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google.list \
    && mkdir -p /usr/share/desktop-directories \
    && apt-get -y update && apt-get install -y google-chrome-stable

# Put Chromedriver into the PATH
ENV PATH $CHROMEDRIVER_DIR:$PATH