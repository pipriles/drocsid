FROM python:3

WORKDIR /home/backend

COPY requirements.txt .
 
RUN pip install --no-cache --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV PORT 5000
ENV REDIS_HOST redis

CMD gunicorn -b 0.0.0.0:$PORT -k eventlet -w 1 wsgi:app
