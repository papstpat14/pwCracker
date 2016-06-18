#!/usr/bin/env python3
import pika
import threading


class ChannelThread(threading.Thread):
    def __init__(self, confdata, reqHandler, confdata_queuename, confdata_routingkey, durable, prefetchCount):
        super(ChannelThread, self).__init__()
        self.confdata = confdata
        self.reqHandler = reqHandler
        self.confdata_queuename = confdata_queuename
        self.confdata_routingkey = confdata_routingkey
        self.durable = durable
        self.prefetchCount = prefetchCount

    def getChannel(self):
        credentials = None
        if (self.confdata['rabbitmq']['username'] is not None) and (self.confdata['rabbitmq']['password'] is not None):
            credentials = pika.PlainCredentials(self.confdata['rabbitmq']['username'],
                                                self.confdata['rabbitmq']['password'])

        parameters = pika.ConnectionParameters(self.confdata['rabbitmq']['host'],
                                               int(self.confdata['rabbitmq']['port']),
                                               self.confdata['rabbitmq']['vhost'],
                                               credentials)

        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        return channel

    def prepareChannel(self, channel):
        exchangename = self.confdata['rabbitmq']['exchangename']
        channel.exchange_declare(exchange=exchangename,
                                 type='direct')

        if (self.confdata_queuename is not None):
            queuename = self.confdata['rabbitmq'][self.confdata_queuename]
            channel.queue_declare(queue=queuename, durable=self.durable)
        else:
            orderqueue = channel.queue_declare(exclusive=True, durable=self.durable)
            queuename = orderqueue.method.queue

        channel.queue_bind(exchange=exchangename,
                           queue=queuename,
                           routing_key=self.confdata['rabbitmq']['routing_keys'][self.confdata_routingkey])
        channel.basic_qos(prefetch_count=self.prefetchCount)
        channel.basic_consume(self.reqHandler.on_request, queue=queuename)

    def run(self):
        channel = self.getChannel()
        self.prepareChannel(channel)
        print("[x] Awaiting RPC requests for routing_key " + self.confdata_routingkey)
        channel.start_consuming()
