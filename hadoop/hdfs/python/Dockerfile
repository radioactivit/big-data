FROM python

WORKDIR ~

RUN pip install virtualenv
RUN easy_install virtualenv
RUN mkdir ~/code
RUN cd ~/code
RUN virtualenv --python=python3 ./venv
RUN pip install fastavro hdfs

RUN apt-get update
RUN apt-get install git nano -y

RUN git clone https://github.com/oc-courses/creez-votre-data-lake

#RUN bash source ~/code/venv/bin/activate

CMD sleep infinity