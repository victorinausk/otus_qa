FROM bitnami/opencart
LABEL maintainer "Victory"

ARG SSH_MASTER_USER
ARG SSH_MASTER_PASS

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    nano \
    sudo \
    openssh-server \
    lftp \
    apt-utils\
    systemd

COPY ssh_config /etc/ssh/ssh_config
COPY sshd_config /etc/ssh/sshd_config

COPY user.sh /usr/local/bin/user.sh
RUN chmod +x /usr/local/bin/user.sh
RUN /usr/local/bin/user.sh
RUN rm /usr/local/bin/user.sh

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD tail -f /dev/null

## Enable mod_ratelimit module
RUN sed -i -r 's/#LoadModule ratelimit_module/LoadModule ratelimit_module/' /opt/bitnami/apache/conf/httpd.conf

## Modify the ports used by Apache by default
# It is also possible to change these environment variables at runtime
ENV APACHE_HTTP_PORT_NUMBER=80
ENV APACHE_HTTPS_PORT_NUMBER=8143
EXPOSE 80 8143