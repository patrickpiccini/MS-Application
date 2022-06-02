#!/usr/bin/python
# -*- encoding: utf-8 -*-

import pika, os

HOST_RABBIT = os.environ['HOST']
# HOST_RABBIT = '144.22.193.219'

class ConnectionRabbitMq():
    
    def __init__(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=HOST_RABBIT, port=5672, heartbeat=10))
            self.channel = self.connection.channel()
            print('[✓] Conected to RabbitMQ server')

        except Exception as error:
            print(f'[X] CONNECTING RABBIT MQ ERROR: {error}')

