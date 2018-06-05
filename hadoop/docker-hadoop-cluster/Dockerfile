FROM ubuntu

WORKDIR /root

RUN apt-get update
RUN apt-get install software-properties-common -y

RUN add-apt-repository ppa:webupd8team/java
RUN apt-get update
#RUN apt-get install oracle-java8-installer wget nano tar -y
RUN apt-get install wget nano tar -y

RUN mkdir code
WORKDIR code
RUN wget http://apache.crihan.fr/dist/hadoop/common/hadoop-2.8.4/hadoop-2.8.4.tar.gz
RUN tar xzf hadoop-2.8.4.tar.gz

CMD sleep infinity