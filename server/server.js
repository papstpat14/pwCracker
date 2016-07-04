//Version: 1.0.0
//LasrChanged: 04.07.2016
//Authors: Michael Koch, Obendrauf Stefan

var http = require("http");
var path = require("path");
var url = require("url");
var fs = require("fs");
var socketServer = require('websocket').server;
var messageHandler = require("./message_handler/messageHandler.js");

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

messageHandler.initSockets(wsServer);