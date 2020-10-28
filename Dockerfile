FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN pip install requests
RUN pip install xmltodict

ENV LISTEN_PORT 10003
EXPOSE 10003


COPY ./app /app
RUN rm -f ./app/users/.gitkeep




