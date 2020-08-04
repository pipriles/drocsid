FROM python:3.8-alpine

COPY requirements.txt .
 
RUN apk update \
    && apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps gcc musl-dev linux-headers

WORKDIR /home/backend

COPY . .

EXPOSE 5000

ENV PORT 5000
ENV REDIS_HOST redis

CMD python wsgi.py
