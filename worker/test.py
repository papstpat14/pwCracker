from time import sleep

import pika
import json
# create json to pass to worker
body = '{"md5":"' + "1c0b76fce779f78f51be339c49445c49" + '"}'
abortbody = '{"md5":"' + "3fc89c714a0bdcaef4ea2fdd23a40527" + '", "action":"stop"}'
# login at server
credentials = pika.PlainCredentials("worker", "worker")
connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.56.101", credentials=credentials))
# create order and reply queues
channel = connection.channel()
channel.exchange_declare(exchange="pw_exchange",type="direct")
replychannel = connection.channel()
replychannel.queue_declare(queue="reply", durable=True)
# read all old messages in reply queue
while True:
    method_frame, header_frame, result = replychannel.basic_get(queue='reply', no_ack=False)
    if method_frame:
        replychannel.basic_ack(method_frame.delivery_tag)
    else:
        break
# publish to order queue
#channel.basic_publish(exchange="pw_exchange", routing_key="order", body=body)
# check if the worker responds correctly
while True:
    # sync read from queue
    method_frame, header_frame, result = replychannel.basic_get(queue='reply', no_ack=False)
    if method_frame:
        result_body = json.loads(result.decode("utf-8"))
        print(result_body)
        replychannel.basic_ack(method_frame.delivery_tag)
        break;
    else:
        sleep(1)
    #    channel.basic_publish(exchange="pw_exchange", routing_key="control", body=abortbody)