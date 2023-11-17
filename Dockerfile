FROM python:3.10
RUN apt-get update

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver-linux64.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/linux64/chromedriver-linux64.zip
RUN unzip /tmp/chromedriver-linux64.zip -d /usr/local/bin/

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN pip install -r /app/edspy/requirements.txt
CMD ["python", "main.py" ]