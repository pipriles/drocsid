# Simple Chat

This is a simple chat application build with Flask, SocketIO, and Redis.  

Users can join the chat by submitting their username and password, notice that if the username does not exist it will be created and other users would not be able to login with that username unless they had the password.

It uses Redis as an in-memory database to store the user data and messages of the room. It only stores the last 50 messages ordered by their timestamp.

A bot is running in the background in a separated process listening to commands in the chat. Users can fetch stock quotes by issuing the command `/stock [CODE]`.

The bot handles exceptions that may occur when fetching the quote or any unexpected behavior.

## Usage

If you have docker installed you can run the application using `docker-compose up` and then going to `http://localhost:5000`.

To run the application without docker you will need to have python 3 and install the dependencies with `pip install -r requirements.txt`. You will also need to have Redis running on port 6379.

To start the server you do `python3 wsgi.py` and to run the bot `python3 bot.py`.

## Tests

To run the tests you will need pytest.

```bash
python -m pytest
```

## TODO

- [x] Setup docker for deployment
- [x] Add `.dockerignore`
- [x] Create simple chat frontend
- [x] Implement simple decoupled bot
- [x] Implement login funcionality
- [x] Implement simple login view
- [x] Add `base.html` template
- [x] Migrate Dockerfiles base image to alpine
- [x] Implement bot authorization token
- [ ] Implement more tests
- [ ] Implement join a room funcionality
- [ ] Use flask blueprints
- [ ] Implement user is typing feature
- [ ] Show current users
- [ ] Run app as non root inside container
- [ ] Support ASCII art
- [ ] Use Redis Publish/Subscribe system?
- [ ] Add password to Redis?
- [ ] Add redis connection mockup?
- [ ] Use aiohttp and asyncio?
