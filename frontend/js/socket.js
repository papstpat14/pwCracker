'use strict';
(function () {
    var ws;
    initSocketConnection();

    function toMessage(md5, pw) {
        return JSON.stringify({
            md5: md5,
            pw: pw
        });
    }

    document.getElementById('crack').onclick = function () {
        initSocketConnection();

        ws.send(toMessage(document.getElementById('hash').value, null));
    };

    function showMessage(message) {
        if (message.md5) {
            if (message.success) {
                document.getElementById('output').innerHTML += '<p style="color: green;"><b>Passwort für ' + message.md5 + ' gefunden von ' + message.workertype + ' : ' + message.pw + '</b></p>';
            } else {
                if (message.success === false) {
                    document.getElementById('output').innerHTML += '<p style="color: red;"><b>Passwort für ' + message.md5 + ' NICHT gefunden von ' + message.workertype + ' - Error: ' + message.err.toString() + '</b></p>';
                } else {
                    document.getElementById('output').innerHTML += '<p>Passwort für ' + message.md5 + ':' + message.pw + '</p>';
                }
            }
        } else {
            console.log('Unsupported message type');
        }
    }

    function initSocketConnection() {
        if (ws) {
            return;
        }

        ws = new WebSocket('ws://'+window.location.host, 'crack-protocol');
        ws.onopen = function () {
            console.log('connected to server!');
        };

        ws.onmessage = function (ev) {
            console.log('< ' + ev.data);
            showMessage(JSON.parse(ev.data));
        };

        ws.onclose = function () {
            console.log('closed');
            ws = null;
        };

        ws.onerror = function () {
            alert('error! could not create socket connection to ws://localhost:8080');
            ws = null;
        };
    }
}());