//Version: 1.0.0
//LasrChanged: 04.07.2016
//Authors: Michael Koch, Obendrauf Stefan

var http = require("http");
var path = require("path");
var url = require("url");
var fs = require("fs");
var amqp = require('amqplib/callback_api');
var socketServer = require('websocket').server;

// Get port from package.json or default 8080
var port = process.env.npm_package_config_port || 8080;

var server = http.createServer(function(req,res){
	// Parse Request
    var requestPath = url.parse(req.url).pathname;
	
	// Check Request Path
	if(requestPath === "/"){
		requestPath = "../frontend/index.html"
	} else if (requestPath.indexOf("/js/") > -1 || requestPath.indexOf("/css/") > -1){
	    requestPath = "../frontend/" + requestPath;
	}
	
	// Join with current working directory
	var fullPath = path.join(process.cwd(),requestPath);
	
	// Look for file
    fs.exists(fullPath,function(exists){
		// Not found -> 404
        if(!exists){
            res.writeHeader(404, {"Content-Type": "text/plain"});  
            res.write("404 Not Found\n");  
            res.end();
        }
		// File found
        else{
            fs.readFile(fullPath, "binary", function(err, file) {  
                 if(err) {  
                     res.writeHeader(500, {"Content-Type": "text/plain"});  
                     res.write(err + "\n");  
                     res.end();  
                
                 }  
                 else{
                    res.writeHeader(200);  
                    res.write(file, "binary");  
                    res.end();
                }
            });
        }
    });
}).listen(port);

console.log("Server Running on port: " + port);        

// Create SocketServer
var wsServer = new socketServer({
    httpServer: server,
    autoAcceptConnections: false
});

var conns = {};
var waitsForHash = {};

var credentials = '';
if (process.env.npm_package_config_rabbitmq_username && process.env.npm_package_config_rabbitmq_password) {
    credentials = process.env.npm_package_config_rabbitmq_username + ':' + process.env.npm_package_config_rabbitmq_password + '@';
}
var rabbitconnstring = 'amqp://' + credentials + process.env.npm_package_config_rabbitmq_host + ':' + process.env.npm_package_config_rabbitmq_port + process.env.npm_package_config_rabbitmq_vhost;
var channel = null;
amqp.connect(rabbitconnstring, function (err, conn) {
        conn.createChannel(function (err, ch) {
                channel = ch;
                ch.assertQueue(process.env.npm_package_config_rabbitmq_replyqueuename, {durable: process.env.npm_package_config_rabbitmq_replyqueuedurable}, function (err, q) {
                    ch.consume(q.queue, function (msg) {
                        console.log(' [.] Got %s', msg.content.toString());
                        var msgObject = JSON.parse(msg.content.toString());
                        if (msgObject.success && (!msgObject.action || msgObject.action == 'get' )) {
                            var requestToRabbit = {
                                'md5': msgObject.md5,
                                'action': 'stop',
                                'pw': msgObject.pw
                            };
                            ch.publish(process.env.npm_package_config_rabbitmq_exchangename, process.env.npm_package_config_rabbitmq_routingkeys_control, new Buffer(JSON.stringify(requestToRabbit)));
                            requestToRabbit.action = 'put';
                            ch.publish(process.env.npm_package_config_rabbitmq_exchangename, process.env.npm_package_config_rabbitmq_routingkeys_order, new Buffer(JSON.stringify(requestToRabbit)));
                            for (var remAdd in waitsForHash[msgObject.md5]) {
                                if (!waitsForHash[msgObject.md5].hasOwnProperty(remAdd)) continue;
                                if (conns[remAdd] && conns[remAdd].conn && conns[remAdd].hash && conns[remAdd].hash == msgObject.md5) {
                                    conns[remAdd].conn.sendUTF(JSON.stringify(msgObject));
                                    if (waitsForHash[msgObject.md5][remAdd]['DB'] != null && waitsForHash[msgObject.md5][remAdd]['Webservice'] != null && waitsForHash[msgObject.md5][remAdd]['Bruteforce'] != null) {
                                        conns[remAdd].hash = null;
                                        delete waitsForHash[msgObject.md5][remAdd];
                                    }
                                }
                            }
                        } else {
                            if (msgObject.success === false) {
                                for (var remAdd in waitsForHash[msgObject.md5]) {
                                    if (!waitsForHash[msgObject.md5].hasOwnProperty(remAdd)) continue;
                                    if (conns[remAdd] && conns[remAdd].conn && conns[remAdd].hash && conns[remAdd].hash == msgObject.md5) {
                                        waitsForHash[msgObject.md5][remAdd][msgObject.workertype] = false;
                                        conns[remAdd].conn.sendUTF(JSON.stringify(msgObject));
                                        if (waitsForHash[msgObject.md5][remAdd]['DB'] != null && waitsForHash[msgObject.md5][remAdd]['Webservice'] != null && waitsForHash[msgObject.md5][remAdd]['Bruteforce'] != null) {
                                            conns[remAdd].hash = null;
                                            delete waitsForHash[msgObject.md5][remAdd];
                                        }
                                    }
                                }
                            }
                        }
                        ch.ack(msg);
                    }, {noAck: false});
                });
                ch.assertExchange(process.env.npm_package_config_rabbitmq_exchangename, 'direct', {durable: false});
            }
        );
    }
);

wsServer.on('request', function (request) {
    var connection = request.accept('crack-protocol', request.origin);
    conns[connection.remoteAddress] = {"conn": connection, "hash": null};
    console.log((new Date()) + ' Connection accepted.');

    connection.on('message', function (message) {
        console.log('Received Message: ' + message.utf8Data);
        var respJSON = JSON.parse(message.utf8Data);
        conns[connection.remoteAddress] = {"conn": connection, "hash": respJSON.md5};
        if (!waitsForHash[respJSON.md5]) {
            waitsForHash[respJSON.md5] = {};
        }
        waitsForHash[respJSON.md5][connection.remoteAddress] = {'DB': null, 'Bruteforce': null, 'Webservice': null};

        var requestToRabbit = {
            'md5': respJSON.md5,
            'action': 'get',
            'success': null,
            'status': 0
        };

        channel.publish(process.env.npm_package_config_rabbitmq_exchangename, 'order', new Buffer(JSON.stringify(requestToRabbit)));
        respJSON.pw = "-- zu ermitteln --";
        connection.sendUTF(JSON.stringify(respJSON));
    });

    connection.on('close', function (connection) {
        if(conns[connection.remoteAddress] && conns[connection.remoteAddress].hash) {
            if(waitsForHash[conns[connection.remoteAddress].hash] && waitsForHash[conns[connection.remoteAddress].hash][connection.remoteAddress]) {
                delete waitsForHash[conns[connection.remoteAddress].hash][connection.remoteAddress];
            }
        }
        delete conns[connection.remoteAddress];
        console.log("Connection close: " + connection);
    });
});