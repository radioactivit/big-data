FROM python:3
WORKDIR /usr/src/app
RUN pip install pika
COPY . .
RUN apt-get update
RUN apt-get install git nano wget -y

CMD sleep infinity