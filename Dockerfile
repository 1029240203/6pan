FROM python:alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY /app /usr/src/app

RUN rm -f /usr/src/app/users/.gitkeep

CMD [ "python", "/usr/src/app/main.py" ]
