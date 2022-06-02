#!/usr/bin/python
# -*- encoding: utf-8 -*-

from config.database_connection import ConnectionDatabase
from config.rabbitmq_connection import ConnectionRabbitMq
from rabbitmq_controller.rabbit_worker import RabbitWorker


class Main():

    def __init__(self):
        self.PSQL = ConnectionDatabase()
        self.RMQ = ConnectionRabbitMq()
        self.RMQ_WORKER = RabbitWorker()

    def consume_queue(self):
        self.RMQ.channel.basic_qos(prefetch_count=1)
        self.RMQ.channel.basic_consume(queue='order', on_message_callback=self.RMQ_WORKER.callback)

        print('     [⇄] Waiting for messages. To exit press CTRL+C')
        self.RMQ.channel.start_consuming()
        
    
if __name__ == '__main__':

    MA = Main()
    MA.consume_queue()
