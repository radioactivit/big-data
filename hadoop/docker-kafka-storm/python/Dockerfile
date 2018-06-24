FROM python

WORKDIR /root

RUN pip install virtualenv
RUN easy_install virtualenv
RUN mkdir /root/code
RUN cd /root/code
RUN virtualenv --python=python3 ./venv
RUN pip install fastavro hdfs kafka-python streamparse

RUN apt-get update
RUN apt-get install git nano wget -y

CMD sleep infinity