import backend

app = backend.create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)

