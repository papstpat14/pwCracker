#!/usr/bin/env python3
import pika
import json
import hashlib

with open('config.json') as conffile:
    confdata = json.load(conffile)

credentials = None
if (confdata['rabbitmq']['username'] is not None) and (confdata['rabbitmq']['password'] is not None):
    credentials = pika.PlainCredentials(confdata['rabbitmq']['username'], confdata['rabbitmq']['password'])

parameters = pika.ConnectionParameters(confdata['rabbitmq']['host'],
                                       int(confdata['rabbitmq']['port']),
                                       confdata['rabbitmq']['vhost'],
                                       credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
exchangename = confdata['rabbitmq']['exchangename']
channel.exchange_declare(exchange=exchangename,
                         type='direct')

with open(confdata['pwlistfilename'], encoding='utf-8') as f:
    for line in f:
        pw = line.rstrip('\n').rstrip('\r')
        if (pw != "" and pw is not None):
            hashval = hashlib.md5(pw.encode('utf-8')).hexdigest()
            req = {'action': 'put', 'md5': hashval, 'pw': pw}
            channel.basic_publish(exchange=exchangename, routing_key='order', body=str(json.dumps(req)))
            print('[.] sent put request to queue for ' + hashval)

channel.queue_declare(queue=confdata['rabbitmq']['replyqueuename'], durable=confdata['rabbitmq']['replyqueuedurable'])


def callback(ch, method, properties, body):
    print("[.] Received %r" % body)


channel.basic_consume(callback, queue=confdata['rabbitmq']['replyqueuename'], no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
