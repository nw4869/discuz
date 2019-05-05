FROM alpine:3.6

# python3
RUN apk --no-cache add python3

# php5
RUN apk --no-cache add php7
RUN ln -sf /usr/bin/php7 /usr/bin/php

# my tools
WORKDIR /discuz
ADD . /discuz
RUN ln -s /discuz/crack.sh /usr/bin/

# php_mt_seed
ADD https://www.openwall.com/php_mt_seed/php_mt_seed-4.0.tar.gz /discuz
RUN tar -xf php_mt_seed-4.0.tar.gz

# gcc & make
RUN apk --no-cache add libgomp
RUN apk --no-cache add --virtual build-dependencies gcc make musl-dev \
  && cd php_mt_seed-4.0 \
  && make \
  && cp php_mt_seed .. \
  && cd .. \
  && ln -s /discuz/php_mt_seed /usr/bin/ \
  && rm -rf php_mt_seed-4.0* \
  && apk del build-dependencies
