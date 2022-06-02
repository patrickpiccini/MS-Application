#!/usr/bin/python
# -*- encoding: utf-8 -*-

import json, pika

from database_controller.postgres_worker import PostgresWorker

class RabbitWorker():

    def __init__(self):
        self.data = ''

    def callback(self, ch, method, props, body):
        self.data = json.loads(body)
        response_work = self.database_manipulation(self.data)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=json.dumps(response_work))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    
    def database_manipulation(self, data):
        # start connection whit postgres
        psql = PostgresWorker()
        if data['type'] == 'create_order':
            print('entrou no type')
            return psql.create_order(data)
        elif data['type'] == 'update_order':
            return psql.edit_order(data)
        elif data['type'] == 'list_all_orders':
            return psql.list_all_orders()
        elif data['type'] == 'list_per_users':
            return psql.list_per_users(data)
        elif data['type'] == 'show_order':
            return psql.show_order(data)
        elif data['type'] == 'delete_order':
            return psql.delete_order(data)

# if __name__ == '__main__':

#     RMQ = RabbitMqCreate()
#     RMQ.recive_queues()
