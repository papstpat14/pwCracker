#!/usr/bin/env python3
import json
import time


class RequestHandler:
    def __init__(self, ph, replyqueuename, pwtimeout):
        self.workingOn = None
        self.ph = ph
        self.replyqueuename = replyqueuename
        self.pwtimeout = pwtimeout
        self.breakcalculation = []

    def on_request(self, ch, method, props, body):
        sendresponse = True
        objRequest = json.loads(body.decode("utf-8"))
        response = {'md5': objRequest['md5'], 'action': objRequest['action'], 'success': None, 'status': 100,
                    'pw': None, 'err': []}

        if ('action' in objRequest):
            if (objRequest['action'] == 'put'):
                print('[.] PUT request for ' + objRequest['md5'])

                self.workingOn = objRequest['md5']
                result = self.ph.putPassword(objRequest['md5'], objRequest['pw'])

                response['success'] = result['success']
                response['pw'] = objRequest['pw']
                response['err'].extend(result['err'])
            elif (objRequest['action'] == 'get'):
                print('[.] GET request for ' + objRequest['md5'])
                self.workingOn = objRequest['md5']

                # Use this to simulate a longer taking process to test stop commands
                time.sleep(self.pwtimeout)

                if (self.breakcalculation and self.workingOn in self.breakcalculation):
                    print('[.] STOPPING request for ' + objRequest['md5'])
                    response['success'] = False
                    response['err'].extend(['Received stop signal'])
                else:
                    result = self.ph.getPassword(objRequest['md5'])

                    response['success'] = result['success']
                    response['pw'] = result['pw']
                    response['err'].extend(result['err'])
            elif (objRequest['action'] == 'stop'):
                print('[.] STOP request for hash ' + objRequest['md5'])

                self.breakcalculation.extend([objRequest['md5']])
                sendresponse = False
            else:
                print("[.] ERROR: action not recognized")

                response['success'] = False
                response['err'].extend(['action not recognized'])
        else:
            print("[.] ERROR: action not set")

            response['success'] = False
            response['err'].extend(['action not set'])

        if (sendresponse):
            ch.basic_publish(exchange='',
                             routing_key=self.replyqueuename,
                             body=str(json.dumps(response)))
            print("[.] RESPONSE Sent: " + str(json.dumps(response)))

        if (response['success'] != None):
            self.workingOn = None
            self.breakcalculation = []

        ch.basic_ack(delivery_tag=method.delivery_tag)
