#!/usr/bin/env python3

import socketio
import requests as rq
import re
import io
import os
import csv

CHAT_HOST = os.environ.get('HOST', 'localhost')
CHAT_PORT = os.environ.get('PORT', 5000)
CHAT_URI  = 'http://{}:{}'.format(CHAT_HOST, CHAT_PORT)

BOT_TOKEN = os.environ.get('BOT_TOKEN', '38f51666d5dffdb15fc06d1ef4dfd0c1ccd1a8daed2b3312')

sio = socketio.Client()

API_URL = 'https://stooq.com/q/l/'

def fetch_stock(code):

    params = { 's': code, 'h': True, 'e': 'csv' }

    try:
        resp = rq.get(API_URL, params=params)
        print(resp.status_code)
        resp.raise_for_status()

    except Exception as e:
        return None

    return resp.text

def send_quotes(stock):

    if stock is None:
        sio.emit('json', {'type': 'misc', 'message': 'Could not fetch stock...' }, namespace='/bot')
        return

    f = io.StringIO(stock)
    reader = csv.DictReader(f)

    for row in reader:

        quote = '{} quote is ${} per share'.format(row['Symbol'], row['Close'])
        sio.emit('json', {'type': 'message', 'message': quote }, namespace='/bot')

def parse_command(command):

    match = re.search(r'/(\w+)\s*=?\s*([\w\.]+)?', command)
    cmd = match.group(1) if match else None
    arg = match.group(2) if match else None

    return cmd, arg

@sio.event
def connect():
    print('Connection Established.')

@sio.event(namespace='/bot')
def message(data):

    if data['type'] == 'command':

        print('Command received', data)

        command = data['message']
        command = command.lower()
        cmd, code = parse_command(command)

        if cmd != 'stock': 
            return

        if code is None:
            sio.emit('json', { 'type': 'misc', 'message': 'Did you miss something?'}, namespace='/bot')
            return

        # Fetch stock CSV data
        stock = fetch_stock(code) 
        send_quotes(stock)

@sio.event
def disconnect():
    print('Disconnected.')

if __name__ == '__main__':
    # Get hostname and port from env
    print('Connecting to', CHAT_URI)
    headers = {'Authorization': 'BotToken ' + BOT_TOKEN } 
    sio.connect(CHAT_URI, headers=headers, namespaces=['/bot'])
    sio.wait()

