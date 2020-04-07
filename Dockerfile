FROM python:3.8

LABEL maintainer="Shlomi Vaknin"

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /
RUN chmod +x /wait-for-it.sh

COPY . /bubbles
RUN pip install /bubbles
