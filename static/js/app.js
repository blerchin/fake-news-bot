if (window.location.protocol === 'https:') {
  var ws_scheme = 'wss://';
} else {
  var ws_scheme = 'ws://'
}

var socket = new ReconnectingWebSocket(ws_scheme + location.host + '/ws' + location.search)

var tweetEl = document.getElementById('tweet');

document.documentElement.style.overflow = 'hidden';

socket.onmessage = function(message) {
  var data = JSON.parse(message.data);
  if (data.evt == 'new:tweet') {
    updateTweet(data.tweet);
  } else {
    console.log(data);
  }
}

socket.onclose = function() {
  console.log('inbox closed')
  this.socket = new WebSocket(socket.url);
}

document.addEventListener('keydown', function(e) {
  if(e.keyCode === 32) {
    socket.send(JSON.stringify({ evt: 'button:pressed' }))
  }
});

function updateTweet(text) {
  var tweet = emoji.parseEmoji(htmlDecode(text));
  tweetEl.innerHTML = tweet;
}

function formatHandles(text) {
  return text.replace(/@([A-Za-z0-9_].*?)/g, function(match, p1) {
    return '; at ' + toCapitalizedWords(p1);
  });
}

function formatHashtags(text) {
  //format hashtags for reading
  return text.replace(/#(.*?)[^A-Za-z0-9]/g, ' hashtag $1 ');
}

function stripUrls(text){
  return text.replace(/https:\/\/(.*?)[^A-Za-z0-9.\/]/g, ' ');
}

function htmlDecode(input) {
  var doc = new DOMParser().parseFromString(input, "text/html");
  return doc.documentElement.textContent;
}
function toCapitalizedWords(name) {
    var words = name.match(/[A-Za-z][a-z]*/g);

    return words.map(capitalize).join(" ");
}

function capitalize(word) {
    return word.charAt(0).toUpperCase() + word.substring(1);
}
