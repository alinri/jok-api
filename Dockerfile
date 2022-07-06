FROM python:3.10.5-slim-buster

WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN apt install -y python3-venv
RUN python3 -m venv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt
RUN pip3 install gunicorn

COPY . /usr/src/app/

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
