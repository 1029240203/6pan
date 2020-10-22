FROM python:alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY /app /usr/src/app

CMD [ "python", "/usr/src/app/main.py" ]
