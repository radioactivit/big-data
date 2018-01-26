FROM java:8
RUN apt-get update && apt-get install -y apt-utils && apt-get install -y procps net-tools iputils-ping nano apt-transport-https
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
RUN echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-6.x.list
RUN apt-get update && apt-get install elasticsearch

CMD sleep infinity