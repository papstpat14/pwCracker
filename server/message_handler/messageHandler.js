var exports = module.exports = {};

// Initiate Websocket Server
function initSocketServer(wsServer){
	// wsServer is not set -> return
	if(!wsServer){
		return;
	}
	
	wsServer.on('request', function (request) {

		var connection = request.accept('chat-protocol', request.origin);
		console.log((new Date()) + ' Connection accepted.');

		connection.on('message', function (message) {
			console.log('Received Message: ' + message.utf8Data);

			var respJSON = JSON.parse(message.utf8Data);
			
			// TODO MessageHandler Team -> implementation for Handling messages
			respJSON.value = "-- zu ermitteln --";
			connection.sendUTF(JSON.stringify(respJSON));
		});

		connection.on('close', function (connection) {
			console.log("Connection close: " + connection);
		});
	});
}

// Export Module with param wsServer
exports.initSockets = function(wsServer){
	initSocketServer(wsServer);
}