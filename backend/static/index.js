(function () {

  var socket = io('/chat')

  let form = document.getElementById('chat-box')
  form.addEventListener('submit', function(event) {

    event.preventDefault();

    let input = document.getElementById('message');
    var mesg  = input.value


    var regex = /\/join[\s=]+(\w+)/g;
    var match = regex.exec(mesg);

    input.value = '';

    if (!!match) {
      var room = match[1];
      console.log('Joining room', room);
      socket.emit('join', { 'room': room });
      location.reload();
      return;
    }

    var payload = { };

    /* if value starts with '/' then is a command */
    payload['type'] = mesg.startsWith('/') ? 'command' : 'message';
    payload['message'] = mesg;

    socket.emit('json', payload);
  });

  socket.on('connect', function() {
    console.log('Connected');
  });

  socket.on('status', function(data) {
    console.log(data);
    var chat = document.getElementById('chat');
    var li   = document.createElement('li');
    li.innerHTML = data['message'];
    chat.appendChild(li);
  });

  socket.on('message', function(data) {
    console.log(data);
    var chat = document.getElementById('chat');
    var li   = document.createElement('li');
    var user = !data['username'] ? 'anonymous' : data['username'];
    li.innerHTML = user + ': ' + data['message'];
    chat.appendChild(li);
  });

})();

