FROM php:5.6-apache

RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list 
RUN echo "deb-src http://archive.debian.org/debian stretch main" >> /etc/apt/sources.list 
RUN echo "deb http://archive.debian.org/debian stretch-backports main" >> /etc/apt/sources.list 
RUN echo  "deb http://archive.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list 
RUN echo  "deb-src http://archive.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list

# https://unix.stackexchange.com/questions/743839/apt-get-update-failed-to-fetch-debian-amd64-packages-while-building-dockerfile-f
# https://daredevel.com/post/2022-03-19-how-to-setup-docker-container-with-legacy-php-5.6-and-xdebug/
RUN apt-get update && \
    apt-get install -y \
    vim \
    libpng-dev \
    gettext


WORKDIR /var/www/html

RUN docker-php-ext-install mysqli gd gettext && docker-php-ext-enable mysqli gd gettext

COPY webERP/ .

RUN chown -R www-data:www-data /var/www/html/

EXPOSE 80