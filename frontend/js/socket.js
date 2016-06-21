"use strict";

var webSocketTest = function () {
    if ("WebSocket" in window) {

        var hash = document.getElementById("hash").value;

        alert("WebSocket is supported by your Browser! Got hash: " + hash);

        // Let us open a web socket
        var ws = new WebSocket("ws://localhost:8080/echo");

        ws.onopen = function () {
            // Web Socket is connected, send data using send()
            ws.send("Message to send");
            alert("Message is sent...");
        };

        ws.onmessage = function (evt) {
            var received_msg = evt.data;
            alert("Message is received...");
        };

        ws.onclose = function () {
            // websocket is closed.
            alert("Connection is closed...");
        };
    }

    else {
        // The browser doesn't support WebSocket
        alert("WebSocket NOT supported by your Browser!");
    }
};

var setupEventListeners = function () {
    document.getElementById("crack").addEventListener("click", webSocketTest);
};

setupEventListeners();