FROM python:3.7

RUN mkdir -p /src

WORKDIR /src

ADD server /src

ADD src /src

ADD requirements.txt /src

#SELENIUM INSTALL

EXPOSE 8000

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99


CMD /bin/bash

RUN pip install regex
RUN pip install pysqlite3
RUN pip install --no-cache-dir -U -r requirements.txt


CMD ["python3", "API.py"]
