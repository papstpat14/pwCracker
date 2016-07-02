var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var bodyParser = require('body-parser');
var socketServer = require('websocket').server;
var routes = require('./routes/index');
var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');


app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use(express.static(path.join(__dirname, '../frontend')));

app.use('/', routes);


app.set('port', process.env.PORT || 8080);

var server = app.listen(app.get('port'), function () {
    console.log('Express server listening on port ' + server.address().port);
});



console.log(__dirname);
var wsServer = new socketServer({
    httpServer: server,
    autoAcceptConnections: false
});

wsServer.on('request', function (request) {

    var connection = request.accept('chat-protocol', request.origin);
    console.log((new Date()) + ' Connection accepted.');

    connection.on('message', function (message) {
        console.log('Received Message: ' + message.utf8Data);

        var respJSON = JSON.parse(message.utf8Data);
        respJSON.value = "-- zu ermitteln --";
        connection.sendUTF(JSON.stringify(respJSON));
    });

    connection.on('close', function (connection) {
        console.log("Connection close: " + connection);
    });
});


// catch 404 and forward to error handler
app.use(function (req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function (err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function (err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});


module.exports = app;
