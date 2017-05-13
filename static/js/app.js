if (window.location.protocol == 'https:') {
  var ws_scheme = 'wss://';
} else {
  var ws_scheme = 'ws://'
}

var inbox = new ReconnectingWebSocket(ws_scheme + location.host + '/receive')
var outbox = new ReconnectingWebSocket(ws_scheme + location.host + '/submit')

var tweetEl = document.getElementById('tweet');

inbox.onmessage = function(message) {
  var data = JSON.parse(message.data);
  if (data.evt == 'new:tweet') {
    tweetEl.textContent = data.tweet;
  } else {
    console.log(data);
  }
}

inbox.onclose = function() {
  console.log('inbox closed')
  this.inbox = new WebSocket(inbox.url);
}

outbox.onclose = function() {
  console.log('outbox close')
  this.outbox = new WebSocket(inbox.url);
}

document.addEventListener('keydown', function(e) {
  if(e.keyCode === 32) {
    outbox.send(JSON.stringify({ evt: 'button:pressed' }))
  }
});
