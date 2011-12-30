// vars
var app = require('express').createServer() // create express server
  , io = require('socket.io').listen(app) // setup socket
  , connections = 0; // number of connections

// init http and socket server on port 80
app.listen(8085);

// app route: index
app.get('/', function (req, res) {
  res.sendfile(__dirname + '/index.html');
});

// app route: assets
app.get('/*.(js|css)', function(req, res){
    res.sendfile('./'+req.url);
});

// on connections
io.sockets.on('connection', function (socket) {
	
	// increase counter and send to clients
	connections++;
	io.sockets.emit('connections', connections);
	
	// socket event: playlist vote
	socket.on('playlist', function (data) {	
		
		// this where you can switch on direction and add votes
		
		// relay the move
		io.sockets.emit('playlist', data);
	});
	
	// socket event: chat
	socket.on('chat', function (data) {
		
		// relay the message
		io.sockets.emit('chat', data);
	});
});

// on disconnect
io.sockets.on('disconnect', function (socket) {
	
	// decrease counter and send to clients
	connections--;
	io.sockets.emit('connections', connections);
});