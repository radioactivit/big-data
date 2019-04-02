FROM ubuntu:latest
LABEL maintainer="Nous"

RUN apt-get update && apt-get install -y apache2

ADD host-apache2.conf /etc/apache2/sites-enabled/000-default.conf
ADD index.html /var/www/test/index.html

EXPOSE 80

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
