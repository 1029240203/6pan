FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN pip install requests

ENV LISTEN_PORT 10003
EXPOSE 10003


COPY ./app /app

VOLUME /app/users



