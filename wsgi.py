#!/usr/bin/env python3 

import backend
import os

app, socketio = backend.create_app()

if __name__ == '__main__':
    port = os.environ.get('PORT')
    socketio.run(app, host='0.0.0.0', port=port, debug=False)

