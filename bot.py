#!/usr/bin/env python3

import socketio
import requests as rq
import re
import io
import csv

sio = socketio.Client()

API_URL = 'https://stooq.com/q/l/'

def fetch_stock(code):

    params = { 's': code, 'h': True, 'e': 'csv' }
    resp = rq.get(API_URL, params=params)

    return resp.text

def send_quotes(stock):

    f = io.StringIO(stock)
    reader = csv.DictReader(f)

    for row in reader:

        quote = '{} quote is ${} per share'.format(row['Symbol'], row['Close'])
        sio.emit('json', {'type': 'message', 'message': quote })

def parse_command(command):

    match = re.search(r'/(\w+)\s*=?\s*([\w\.]+)?', command)
    cmd = match.group(1)
    arg = match.group(2)

    return cmd, arg

@sio.event
def connect():
    print('Connection Established.')

@sio.event
def message(data):

    if data['type'] == 'command':

        print('Command received', data)

        command = data['message']
        command = command.lower()
        cmd, code = parse_command(command)

        if cmd != 'stock': 
            return

        if code is None:
            sio.emit('json', { 'type': 'misc', 'message': 'Did you misspelled something?'})
            return

        # Fetch stock CSV data
        stock = fetch_stock(code) 
        send_quotes(stock)

@sio.event
def disconnect():
    print('Disconnected.')

if __name__ == '__main__':
    # Get hostname and port from env
    sio.connect('http://localhost:5000', namespaces=['/bot'])
    sio.wait()

