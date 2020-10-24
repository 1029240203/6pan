FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN pip install requests


ENV LISTEN_PORT 10003
EXPOSE 10003

VOLUME /app

RUN rm -f ./app/users/.gitkeep
COPY ./app /app




