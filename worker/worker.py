#!/usr/bin/env python3.4
import json
import threading

from worker_type import call_api
from worker_type import brute_force
from sys import argv
import pika

# edit the this config parameters
host = "locahost"
orderQueue = "order"
replyQueue = "reply"
controlQueue = "control"
user="worker"
password="worker"
stoppedCalc={}
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
    body_string = body.decode("utf-8");
    stoppedCalc[json.loads(body_string)["md5"]]=0
    obj = func(body_string,stoppedCalc)
    send_reply(obj)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def callbackControl(ch, method, properties, body):
    controlMessage = json.loads(body.decode("utf-8"));
    if(controlMessage["action"]=="stop"):
        stoppedCalc[controlMessage["md5"]]=1

def send_reply(obj):
    con = pika.BlockingConnection(pika.ConnectionParameters(host=host,credentials=credentials))
    cha = con.channel()
    cha.queue_declare(queue=replyQueue, durable=True)
    text = json.dumps(obj.__dict__)
    cha.basic_publish(exchange="", routing_key=replyQueue, body=text)
    con.close()

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=orderQueue)
#run order queue in another thread
t = threading.Thread (target=channel.start_consuming)
t.daemon=True
t.start()
#start control queue
controlConnection = pika.BlockingConnection(pika.ConnectionParameters(host=host,credentials=credentials))
controlChannel = controlConnection.channel()
controlChannel.queue_declare(queue=controlQueue,durable=True)
controlChannel.basic_consume(callbackControl, queue=controlQueue)
controlChannel.start_consuming()
