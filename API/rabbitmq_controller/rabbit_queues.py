
#!/usr/bin/python
# -*- encoding: utf-8 -*-

import pika, uuid, threading, time
from config.rabbitmq_connection import RabbitConnection

class RabbitQueue():
    internal_lock = threading.Lock()
    queue = {}

    def __init__(self) :
        self.RMQ = RabbitConnection()
        result = self.RMQ.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self._create_process_thread()

    def create_queues(self):
        self.RMQ.channel.queue_declare(queue='user')
        self.RMQ.channel.queue_declare(queue='order')
        
        print('     [✓] Queues created successful!')


    def rpc_async(self, payload, route):
        corr_id = str(uuid.uuid4())
        self.queue[corr_id] = None
        with self.internal_lock:
            self.RMQ.channel.basic_publish(exchange='',
                                       routing_key=route,
                                       properties=pika.BasicProperties(
                                           reply_to=self.callback_queue,
                                           correlation_id=corr_id,
                                       ),
                                       body=payload)
        return corr_id

    def _create_process_thread(self):
        thread = threading.Thread(target=self._process_data_events)
        thread.setDaemon(True)
        thread.start()

    def _process_data_events(self):
        self.RMQ.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self._on_response, 
            auto_ack=True,
        )

        while True:
            with self.internal_lock:
                self.RMQ.connection.process_data_events()
                time.sleep(0.1)

    def _on_response(self, ch, method, props, body):
        """On response we simply store the result in a local dictionary."""
        self.queue[props.correlation_id] = body
