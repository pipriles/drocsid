#!/usr/bin/env python3 

import backend

app, socketio = backend.create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=False)

