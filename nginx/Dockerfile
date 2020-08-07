FROM nginx

RUN mkdir -p conf.d
RUN mkdir -p /var/www/html/.well-known/acme-challenge
RUN mkdir -p /etc/letsencrypt
RUN rm etc/nginx/conf.d/*

COPY *.conf /etc/nginx/conf.d/
COPY letsencrypt.tar.gz /home/ubuntu/

RUN tar -xzvf /home/ubuntu/letsencrypt.tar.gz
RUN cp -r letsencrypt/* /etc/letsencrypt

EXPOSE 80
EXPOSE 443
