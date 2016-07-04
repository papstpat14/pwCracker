var exports = module.exports = {};

// Initiate Websocket Server
function initSocketServer(wsServer){
	// wsServer is not set -> return
	if(!wsServer){
		return;
	}
	
	wsServer.on('request', function (request) {

		var connection = request.accept('crack-protocol', request.origin);
		console.log((new Date()) + ' Connection accepted.');

		connection.on('message', function (message) {
			var respJSON = JSON.parse(message.utf8Data);

			// TODO MessageHandler Team -> implementation for Handling messages
			respJSON.value = "-- zu ermitteln --";
			console.log('Received Message: ' + message.utf8Data);

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