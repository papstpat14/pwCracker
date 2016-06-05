#!/usr/bin/env python3.4
import json
from worker_type import call_api
from worker_type import brute_force
from sys import argv
import pika

# edit the this config parameters
host = "locahost"
orderQueue = "order"
replyQueue = "reply"
user="worker"
password="worker"
# ----------------------------------------------------------------

func = None
if len(argv) < 2 or len(argv) > 3:
    raise ValueError("illegal cmd line argument, use -b for brute_force or -w for web service instead")
elif argv[1] == "-b":
    func = brute_force
elif argv[1] == "-w":
    func = call_api
else:
    raise ValueError("illegal cmd line argument: " + argv[1] + ", use -b for brute_force or -w for web service instead")

if len(argv) > 2:
        host=argv[2];
credentials = pika.PlainCredentials(user, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue=orderQueue, durable=True)


def callback(ch, method, properties, body):
    obj = func(body.decode("utf-8"))
    send_reply(obj)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def send_reply(obj):
    con = pika.BlockingConnection(pika.ConnectionParameters(host=host,credentials=credentials))
    cha = con.channel()
    cha.queue_declare(queue=replyQueue, durable=True)
    text = json.dumps(obj.__dict__)
    cha.basic_publish(exchange="", routing_key=replyQueue, body=text)
    con.close()

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=orderQueue)
channel.start_consuming()
