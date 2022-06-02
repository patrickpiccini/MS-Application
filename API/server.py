#!/usr/bin/python
# -*- encoding: utf-8 -*-

import json, time
from flask import Flask, request
from flask_caching import Cache  # Import Cache from flask_caching module
from config.database_connection import ConnectionDatabase
from rabbitmq_controller.rabbit_queues import RabbitQueue


rabbit_queues = RabbitQueue()


class Api_server():

    app = Flask(__name__)
    app.config.from_object('config.redis_connection.BaseConfig')
    cache = Cache(app)  # Initialize Cache

    ConnectionDatabase()
    rabbit_queues.create_queues()

    # ---------------User Routes----------------
    @app.route("/user/create_user/", methods=['POST'])
    def create_user():
        if request.method == 'POST':
            payload = request.get_json()
            payload['type'] = 'create'

            corr_id = rabbit_queues.rpc_async(json.dumps(payload), "user")
            while rabbit_queues.queue[corr_id] is None:
                time.sleep(0.1)

            return {'Status': 200, 'Message': json.loads(rabbit_queues.queue[corr_id])}
        else:
            return {'Status': 404, 'Message': 'Erro no envio do method'}

    @app.route("/user/show_all_user/", methods=['GET'])
    @cache.cached(timeout=30, query_string=True)
    def list_user():
        if request.method == 'GET':
            payload = {'type': 'show_all'}

            corr_id = rabbit_queues.rpc_async(json.dumps(payload), "user")
            while rabbit_queues.queue[corr_id] is None:
                time.sleep(0.1)

            return {'Status': 200, 'All Users': json.loads(rabbit_queues.queue[corr_id])}
        else:
            return {'Status': 404, 'Message': 'Erro no envio do method'}

    @app.route("/user/show_one_user/", methods=['POST'])
    @cache.cached(timeout=30, query_string=True)
    def show_user():
        if request.method == 'POST':
            payload = request.get_json()
            payload['type'] = 'show_one'

            corr_id = rabbit_queues.rpc_async(json.dumps(payload), "user")
            while rabbit_queues.queue[corr_id] is None:
                time.sleep(0.1)

            return {'Status': 200, 'Message': json.loads(rabbit_queues.queue[corr_id])}
        else:
            return {'Status': 404, 'Message': 'Erro no envio do method'}

    @app.route("/user/edit_user/", methods=['PUT'])
    def edit_user():
        if request.method == 'PUT':
            payload = request.get_json()
            payload['type'] = 'update'

            corr_id = rabbit_queues.rpc_async(json.dumps(payload), "user")
            while rabbit_queues.queue[corr_id] is None:
                time.sleep(0.1)

            return {'Status': 200, 'Message': json.loads(rabbit_queues.queue[corr_id])}
        else:
            return {'Status': 404, 'Message': 'Erro no envio do method'}

    @app.route("/user/edit_password/", methods=['PUT'])
    def edit_password():
        if request.method == 'PUT':
            payload = request.get_json()
            payload['type'] = 'update_password'

            corr_id = rabbit_queues.rpc_async(json.dumps(payload), "user")
            while rabbit_queues.queue[corr_id] is None:
                time.sleep(0.1)

            return {'Status': 200, 'Message': json.loads(rabbit_queues.queue[corr_id])}
        else:
            return {'Status': 404, 'Message': 'Erro no envio do method'}

    @app.route("/user/delete_user/", methods=['DELETE'])
    def delete_user():
        if request.method == 'DELETE':
            payload = request.get_json()
            payload['type'] = 'delete_user'

            corr_id = rabbit_queues.rpc_async(json.dumps(payload), "user")
            while rabbit_queues.queue[corr_id] is None:
                time.sleep(0.1)

            return {'Status': 200, 'Message': json.loads(rabbit_queues.queue[corr_id])}
        else:
            return {'Status': 404, 'Message': 'Erro no envio do method'}

    # -----------------Order Routes-----------------

    @app.route("/order/create_order/", methods=['POST'])
    def create_order():
        if request.method == 'POST':
            payload = request.get_json()
            payload['type'] = 'create_order'

            corr_id = rabbit_queues.rpc_async(json.dumps(payload), "order")
            while rabbit_queues.queue[corr_id] is None:
                time.sleep(0.1)

            return {'Status': 200, 'Message': json.loads(rabbit_queues.queue[corr_id])}
        else:
            return {'Status': 404, 'Message': 'Erro no envio do method'}

    @app.route("/order/list_all_orders/", methods=['GET'])
    @cache.cached(timeout=30, query_string=True)
    def list_order():
        if request.method == 'GET':
            payload = {'type': 'list_all_orders'}

            corr_id = rabbit_queues.rpc_async(json.dumps(payload), "order")
            while rabbit_queues.queue[corr_id] is None:
                time.sleep(0.1)

            return {'Status': 200, 'Orders': json.loads(rabbit_queues.queue[corr_id])}
        else:
            return {'Status': 404, 'Message': 'Erro no envio do method'}

    @app.route("/order/list_per_users/", methods=['GET'])
    @cache.cached(timeout=30, query_string=True)
    def list_per_users():
        if request.method == 'GET':
            payload = request.get_json()
            payload['type']= 'list_per_users'

            corr_id = rabbit_queues.rpc_async(json.dumps(payload), "order")
            while rabbit_queues.queue[corr_id] is None:
                time.sleep(0.1)

            return {'Status': 200, 'Orders': json.loads(rabbit_queues.queue[corr_id])}
        else:
            return {'Status': 404, 'Message': 'Erro no envio do method'}

    @app.route("/order/show_order/", methods=['GET'])
    @cache.cached(timeout=30, query_string=True)
    def show_order():
        if request.method == 'GET':
            payload = request.get_json()
            payload['type']= 'show_order'

            corr_id = rabbit_queues.rpc_async(json.dumps(payload), "order")
            while rabbit_queues.queue[corr_id] is None:
                time.sleep(0.1)

            return {'Status': 200, 'Orders': json.loads(rabbit_queues.queue[corr_id])}
        else:
            return {'Status': 404, 'Message': 'Erro no envio do method'}

    @app.route("/order/update_order/", methods=['PUT'])
    def update_order():
        if request.method == 'PUT':
            payload = request.get_json()
            payload['type'] = 'update_order'

            corr_id = rabbit_queues.rpc_async(json.dumps(payload), "order")
            while rabbit_queues.queue[corr_id] is None:
                time.sleep(0.1)

            return {'Status': 200, 'Order': json.loads(rabbit_queues.queue[corr_id])}
        else:
            return {'Status': 404, 'Message': 'Erro no envio do method'}


    @app.route("/order/delete_order/", methods=['DELETE'])
    def delete_order():
        if request.method == 'DELETE':
            payload = request.get_json()
            payload['type'] = 'delete_order'

            corr_id = rabbit_queues.rpc_async(json.dumps(payload), "order")
            while rabbit_queues.queue[corr_id] is None:
                time.sleep(0.1)

            return {'Status': 200, 'Order': json.loads(rabbit_queues.queue[corr_id])}
        else:
            return {'Status': 404, 'Message': 'Erro no envio do method'}

    app.run('0.0.0.0', 7000)


# if __name__ == '__main__':

#     APP = Api_server()
#     APP.app.run('0.0.0.0', 7000)
