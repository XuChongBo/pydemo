FROM docker.zuoyetong.com.cn/python:2.7-slim
MAINTAINER "XuChongBo <xcbfreedom@gmail.com>"

COPY ./requirements.txt /
ADD http://docker.zuoyetong.com.cn/build/jessie-sources.list /etc/apt/sources.list
RUN apt-get update \
    && apt-get install -y curl \
    && pip install -r requirements.txt \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

ADD . /code
WORKDIR /code
RUN mkdir /logs

CMD ./run-site.sh
