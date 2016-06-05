import os
import signal
import subprocess
import unittest
from time import sleep

import pika
import json

import sys
from worker_type import call_api
from worker_type import brute_force


class ApiTestCase(unittest.TestCase):
    def test_call_api(self):
        self.call_worker_type(self, "1c0b76fce779f78f51be339c49445c49", "secure", call_api)
        self.call_worker_type(self, "3fc89c714a0bdcaef4ea2fdd23a40527", "IAmTheHodor39@", call_api)

    def test_brute_force(self):
        self.call_worker_type(self, "128ecf542a35ac5270a87dc740918404", "bla", brute_force)
        self.call_worker_type(self, "187ef4436122d1cc2f40dc2b92f0eba0", "ab", brute_force)

    def test_worker_queue_force(self):
        #start the worker
        pid = self.start_worker(self,"-b", "192.168.56.101")
        #send him the message
        self.queue_worker_job(self,"187ef4436122d1cc2f40dc2b92f0eba0", "ab")
        self.queue_worker_job(self,"128ecf542a35ac5270a87dc740918404", "bla")
        #stop the worker
        self.stop_worker(self,pid)

    def test_worker_queue_api(self):
        #start the worker
        pid = self.start_worker(self,"-w", "192.168.56.101")
        #send him the message
        self.queue_worker_job(self,"1c0b76fce779f78f51be339c49445c49", "secure")
        self.queue_worker_job(self,"3fc89c714a0bdcaef4ea2fdd23a40527", "IAmTheHodor39@")
        #stop the worker
        self.stop_worker(self,pid)

    def test_worker_queue_abort(self):
        # start the worker
        pid = self.start_worker(self, "-b", "192.168.56.101")
        #send the impossible task
        self.queue_worker_job(self,"3fc89c714a0bdcaef4ea2fdd23a40527", "IAmTheHodor39@","Worker aborted",True)
        # stop the worker
        self.stop_worker(self, pid)

    @staticmethod
    def start_worker(x,mode,host):
        pid = subprocess.Popen([sys.executable, os.path.dirname(__file__)+"/worker.py",mode,host]).pid
        return pid

    @staticmethod
    def stop_worker(x,pid):
        os.kill(pid,signal.SIGTERM)

    @staticmethod
    def queue_worker_job(x,md5,pw,err=None,abort=False):
        #create json to pass to worker
        body = '{"md5":"' + md5 + '"}'
        abortbody='{"md5":"'+md5+'", "action":"stop"}'
        #login at server
        credentials = pika.PlainCredentials("worker", "worker")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.56.101", credentials=credentials))
        #create order and reply queues
        channel = connection.channel()
        channel.queue_declare(queue="order", durable=True)
        channel.queue_declare(queue="control",durable=True)
        replychannel = connection.channel()
        replychannel.queue_declare(queue="reply", durable=True)
        #read all old messages in reply queue
        while True:
            method_frame, header_frame, result = replychannel.basic_get(queue='reply', no_ack=False)
            if method_frame:
                replychannel.basic_ack(method_frame.delivery_tag)
            else:
                break
        #publish to order queue
        channel.basic_publish(exchange="", routing_key="order", body=body)
        #check if the worker responds correctly
        while True:
            #sync read from queue
            method_frame,header_frame,result = replychannel.basic_get(queue='reply', no_ack=False)
            if method_frame:
                result_body=json.loads(result.decode("utf-8"))
                if(err!=None):
                    x.assertEqual(result_body["err"],err)
                else:
                    x.assertEqual(result_body["success"], True)
                    x.assertEqual(result_body["md5"], md5)
                    x.assertEqual(result_body["pw"], pw)
                    x.assertEqual(result_body["err"], "")
                replychannel.basic_ack(method_frame.delivery_tag)
                break;
            else:
                sleep(1)
                #if abort is requested abort after 1 second
                if(abort):
                    channel.basic_publish(exchange="",routing_key="control",body=abortbody)

    @staticmethod
    def call_worker_type(x, md5, pw, func):
        controlList={}
        controlList[md5]=0
        body = '{"md5":"' + md5 + '"}'
        obj = func(body,controlList)
        x.assertEqual(obj.success, True)
        x.assertEqual(obj.md5, md5)
        x.assertEqual(obj.pw, pw)
        x.assertEqual(obj.err, "")


if __name__ == '__main__':
    unittest.main()
