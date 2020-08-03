FROM python:3.5-alpine

COPY requirements.txt .
 
RUN apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps gcc musl-dev linux-headers

WORKDIR /home/backend

COPY . .

EXPOSE 5000

ENV PORT 5000
ENV REDIS_HOST redis

CMD gunicorn -b 0.0.0.0:$PORT -k eventlet -w 1 wsgi:app
