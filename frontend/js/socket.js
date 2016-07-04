'use strict';
(function () {
    var username;

    var ws;
    initSocketConnection();

    function toMessage(type, hash) {
        return JSON.stringify({
            type: type,
            hash: hash
        });
    }

    document.getElementById('crack').onclick = function () {
        initSocketConnection();

        ws.send(toMessage('md5', document.getElementById('hash').value));
    };

    function showMessage(message) {
        if (message.type === 'md5') {
            document.getElementById('output').innerHTML += '<p>' + message.hash + ' : ' + message.value + '</p>';
        } else {
            console.log('Unsupported message type: ' + message.type);
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