FROM php:8.1-apache

RUN apt-get update && \
    apt-get install -y \
    vim \
    libpng-dev \
    default-mysql-client


WORKDIR /var/www/html

RUN docker-php-ext-install mysqli gd gettext pdo pdo_mysql opcache
RUN docker-php-ext-enable mysqli gd gettext pdo pdo_mysql opcache

COPY phpfusion/ .

RUN chown -R www-data:www-data /var/www/html/

EXPOSE 80