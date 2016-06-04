#!/usr/bin/env node

var fs = require('fs');
var args = process.argv.slice(2);

if (args.length >= 2 && args.length <= 3 && args[0].toString() == "test") {
    var countTests = 1;
    if (args.length == 3) {
        countTests = args[2];
    }
    var to_md5 = require('md5');
    var passwords = [
        "Ausschau",
        "nico",
        "patrick",
        "kager",
        "passwort",
        "fhjoanneum",
        "einfach",
        "12345",
        "spannend"
    ];

    var amqp = require('amqplib/callback_api');

    var md5 = {};

    var settingsFileContent = fs.readFileSync("../config.json");
    var jsonSettings = JSON.parse(settingsFileContent);

    var credentials = '';
    if (jsonSettings.rabbitmq.username && jsonSettings.rabbitmq.password) {
        credentials = jsonSettings.rabbitmq.username + ':' + jsonSettings.rabbitmq.password + '@';
    }
    var rabbitconnstring = 'amqp://' + credentials + jsonSettings.rabbitmq.host + ':' + jsonSettings.rabbitmq.port + jsonSettings.rabbitmq.vhost;

    amqp.connect(rabbitconnstring, function (err, conn) {
            conn.createChannel(function (err, ch) {
                    ch.assertQueue(jsonSettings.rabbitmq.replyqueuename, {durable: jsonSettings.rabbitmq.replyqueuedurable}, function (err, q) {
                        ch.consume(q.queue, function (msg) {
                            console.log(' [.] Got %s', msg.content.toString());
                        }, {noAck: true});
                    });
                    ch.assertExchange(jsonSettings.rabbitmq.exchangename, 'direct', {durable: false});
                    if (args[1].toString() == "get") {
                        for (var i = 0; i < countTests; i++) {
                            for (var index = 0; index < passwords.length; index++) {
                                md5.md5 = to_md5(passwords[index]);
                                md5.action = 'get';
                                console.log(' [x] Requesting md5crack(%s)', JSON.stringify(md5));
                                ch.publish(jsonSettings.rabbitmq.exchangename, 'order', new Buffer(JSON.stringify(md5)));
                            }
                        }
                    } else if (args[1].toString() == "put") {
                        for (var i = 0; i < countTests; i++) {
                            for (var index = 0; index < passwords.length; index++) {
                                md5.md5 = to_md5(passwords[index]);
                                md5.pw = passwords[index];
                                md5.action = 'put';
                                console.log(' [x] Requesting put(%s)', JSON.stringify(md5));
                                ch.publish(jsonSettings.rabbitmq.exchangename, 'order', new Buffer(JSON.stringify(md5)));
                            }
                        }
                    } else {
                        for (var index = 0; index < passwords.length; index++) {
                            md5.md5 = to_md5(passwords[index]);
                            md5.pw = passwords[index];
                            md5.action = 'stop';
                            console.log(' [x] Requesting stop(%s)', JSON.stringify(md5));
                            ch.publish(jsonSettings.rabbitmq.exchangename, 'control', new Buffer(JSON.stringify(md5)));
                        }
                    }
                }
            );
        }
    );
}