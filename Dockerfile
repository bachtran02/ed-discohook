FROM python:3.10
RUN apt-get update

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN pip install -r /app/edspy/requirements.txt
CMD ["python", "main.py" ]