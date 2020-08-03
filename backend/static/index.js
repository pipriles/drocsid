(function () {

  var socket = io()

  let form = document.getElementById('chat-box')
  form.addEventListener('submit', function(event) {
    event.preventDefault();
    let input = document.getElementById('message');
    var mesg  = input.value
    socket.emit('json', { type: 'message', message: mesg });
  });

  socket.on('connect', function() {
    console.log('Connected');
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

