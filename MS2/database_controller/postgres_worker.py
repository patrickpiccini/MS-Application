#!/usr/bin/python
# -*- encoding: utf-8 -*-

from config.database_connection import ConnectionDatabase
from datetime import datetime


class PostgresWorker():

    def __init__(self):
        self.PSQL = ConnectionDatabase()
        self.date_time = datetime.now()
        self.date_time_formate = self.date_time.strftime('%Y/%m/%d %H:%M')

    # create a order in database
    def create_order(self, data):
        try:
            user_id = self.information_user(data['nick_name'])
            if user_id == None:
                return f"[X] DON'T HAVE THIS USER IN DATA-BASE!"

            total_value = data['item_quantity'] * data['item_price']

            query_insert = 'INSERT INTO orders (user_id ,item_description ,item_quantity , item_price, total_value, created_at, updated_at)VALUES (%s,%s,%s,%s,%s,%s,%s)'
            vars_query = (user_id[0], data['item_description'], data['item_quantity'],
                          data['item_price'], total_value, self.date_time_formate, self.date_time_formate)
            self.PSQL.cursor.execute(query_insert, vars_query)
            self.PSQL.connection.commit()

            print('[✓] INSERTION DONE IN POSTGRES!')
            return '[✓] Order created successfully! '
        except Exception as error:
            print(error)
            return f'[X] ERROR INSERTING IN POSTGRES! {error}'
        finally:
            self.PSQL.cursor.close()
        pass

    # Modify the informations of a order
    def edit_order(self, data):
        try:
            user_id = self.information_user(data['nick_name'])
            if user_id == None:
                return f"[X] DON'T HAVE THIS USER IN DATA-BASE!"

            total_value = data['item_quantity'] * data['item_price']
            
            query_update = 'UPDATE orders SET user_id=%s, item_description=%s, item_quantity=%s, item_price=%s, total_value=%s, updated_at=%s WHERE order_id=%s'
            vars_query = (user_id[0], data['item_description'], data['item_quantity'],
                          data['item_price'], total_value, self.date_time_formate, data['order_id'])
            self.PSQL.cursor.execute(query_update, vars_query)
            self.PSQL.connection.commit()
            row_count = self.PSQL.cursor.rowcount
            record = self.information_order(data['order_id'])

            if record == None:
                return f'[X] {record} - Nenhum chamado encontrado com o id {data["order_id"]}'

            dict_response = {
                'Altered Lines': row_count,
                'order_id': record[0],
                'user_id': record[1],
                'item_description': record[2],
                'item_quantity': record[3],
                'item_price': record[4],
                'total_value': record[5],
                'created_at': str(record[6]),
                'updated_at': str(record[7])
            }
            print('[✓] UPDADE DONE SUCCESSFULLY IN POSTGRES!')
            return dict_response
        except Exception as error:
            print(error)
            return f'[X] ERROR IN UPDATED ORDER INFORMATION IN POSTGRES! {error}'
        finally:
            self.PSQL.cursor.close()

    # Show all orders of batabase
    def list_all_orders(self):
        try:
            sql_select_query = 'SELECT order_id, item_description FROM orders'
            self.PSQL.cursor.execute(sql_select_query)
            record = self.PSQL.cursor.fetchall()
            self.PSQL.connection.commit()

            dict_all_orders = []
            for index in range(len(record)):
                dict_respose={
                    'order_id': record[index][0],
                    'item_description': record[index][1],
                }
                dict_all_orders.append(dict_respose)

            print('[✓] SELECT ALL USER DONE SUCCESSFULLY IN POSTGRES!')
            return dict_all_orders
        except Exception as error:
            print(error)
            return f'[X] ERROR ON SELECT IN POSTGRES! {error}'
        finally:
            self.PSQL.cursor.close()

    # Show orders per users in batabase
    def list_per_users(self, data):
        try:
            user_id = self.information_user(data['nick_name'])
            if user_id == None:
                return f"[X] DON'T HAVE THIS USER IN DATA-BASE!"
            
            sql_select_query = 'SELECT * FROM orders WHERE user_id=%s'
            vars_query_select = user_id[0]
            self.PSQL.cursor.execute(sql_select_query, (vars_query_select,))
            record = self.PSQL.cursor.fetchall()
            self.PSQL.connection.commit()

            dict_all_orders = []
            for index in range(len(record)):
                dict_response = {
                    'order_id': record[index][0],
                    'nick_name': data['nick_name'],
                    'item_description': record[index][2],
                    'item_quantity': record[index][3],
                    'item_price': record[index][4],
                    'total_value': record[index][5],
                    'created_at': str(record[index][6]),
                    'updated_at': str(record[index][7])
                }
                dict_all_orders.append(dict_response)

            print('[✓] SELECT FOR USER DONE SUCCESSFULLY IN POSTGRES!')
            return dict_all_orders
        except Exception as error:
            print(error)
            return f'[X] ERROR ON SELECT IN POSTGRES! {error}'
        finally:
            self.PSQL.cursor.close()

    # Show a order by ID
    def show_order(self, data):
        try:
            record = self.information_order(data['order_id'])

            if record == None:
                return f'[X] {record} - Nenhum chamado encontrado com o id {data["order_id"]}'

            dict_response = {
                'order_id': record[0],
                'user_id': record[1],
                'item_description': record[2],
                'item_quantity': record[3],
                'item_price': record[4],
                'total_value': record[5],
                'created_at': str(record[6]),
                'updated_at': str(record[7])
            }
            print('[✓] UPDADE DONE SUCCESSFULLY IN POSTGRES!')
            return dict_response
        except Exception as error:
            print(error)
            return f'[X] ERROR IN UPDATED ORDER INFORMATION IN POSTGRES! {error}'
        finally:
            self.PSQL.cursor.close()

    # Delete a order on database
    def delete_order(self, data):
        try:
            sql_delete_query = 'DELETE FROM orders WHERE order_id=%s'
            vars_query_select = data['order_id']
            self.PSQL.cursor.execute(sql_delete_query, (vars_query_select,))
            row_count = self.PSQL.cursor.rowcount
            self.PSQL.connection.commit()
        
            print('[✓] DELETE DONE SUCCESSFULLY IN POSTGRES!')
            return {'Altered Lines': row_count}
        except Exception as error:
            print(error)
            return f'[X] ERROR ON DELETE IN POSTGRES! {error}'
        finally:
            self.PSQL.cursor.close()

    # get all user's ID on database
    def information_user(self, data):
        try:
            sql_select_query = 'SELECT user_id FROM users WHERE nick_name=%s'
            vars_query_select = data
            self.PSQL.cursor.execute(sql_select_query, (vars_query_select,))
            record = self.PSQL.cursor.fetchone()
            return record
        except Exception as error:
            print(error)
            return f'[X] ERROR ON SELECT ID_USER IN POSTGRES! \
        {error}'

    
     # get all order's irformation on database
    def information_order(self, data):
        try:
            sql_select_query = 'SELECT * FROM orders WHERE order_id=%s'
            vars_query_select = data
            self.PSQL.cursor.execute(sql_select_query, (vars_query_select,))
            record = self.PSQL.cursor.fetchone()

            return record
        except Exception as error:
            print(error)
            return f'[X] ERROR ON SELECT ORDER INFORMATION IN POSTGRES! \
        {error}'
        finally:
            self.PSQL.cursor.close()

    
