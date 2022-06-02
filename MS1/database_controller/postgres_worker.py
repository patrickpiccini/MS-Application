
from config.database_connection import ConnectionDatabase
from criptografy.hash_password import EncriptPassword
from datetime import datetime


class PostgresWorker():

    def __init__(self):
        self.PSQL = ConnectionDatabase()
        self.date_time = datetime.now()
        self.date_time_formate = self.date_time.strftime('%Y/%m/%d %H:%M')

    # create a user in database
    def insert_user(self, data):
        try:
            encripted_password = self.encript_password(data['password'])

            query_insert = 'INSERT INTO users (full_name, nick_name ,password ,cpf , email, phone_number, created_at, updated_at)VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
            vars_query = (data['name'], data['nick_name'], encripted_password, data['cpf'],
                          data['email'], data['phone_number'], self.date_time_formate, self.date_time_formate)
            self.PSQL.cursor.execute(query_insert, vars_query)
            self.PSQL.connection.commit()

            print('[✓] INSERTION DONE IN POSTGRES!')
            return '[✓] User created successfully! '
        except Exception as error:
            print(error)
            return f'[X] ERROR INSERTING IN POSTGRES! {error}'
        finally:
            self.PSQL.cursor.close()

    # Modify the informations of a user
    def alter_user(self, data):
        try:
            result_psw = self.take_pass(data['nick_name'])
            verify = self.verify_password_database(
                result_psw, data['password'])

            if verify == False:
                return f'[X] PASSWORD NOT EQUAL!'

            query_update = 'UPDATE users SET full_name=%s ,cpf=%s , email=%s, phone_number=%s, updated_at=%s WHERE nick_name=%s'
            vars_query = (data['name'], data['cpf'], data['email'],
                          data['phone_number'], self.date_time_formate, data['nick_name'])
            self.PSQL.cursor.execute(query_update, vars_query)
            self.PSQL.connection.commit()
            row_count = self.PSQL.cursor.rowcount
            record = self.information_user(data['nick_name'])

            if record == None:
                return record

            dict_response = {
                'Altered Lines': row_count,
                'nick_name': record[1],
                'name': record[3],
                'password': record[2],
                'cpf': record[4],
                'email': record[5],
                'phone_number': record[6],
                'created_at': str(record[7]),
                'updated_at': str(record[8])
            }
            print('[✓] UPDADE DONE SUCCESSFULLY IN POSTGRES!')
            return dict_response
        except Exception as error:
            print(error)
            return f'[X] ERROR IN UPDATED USER INFORMATION IN POSTGRES! {error}'
        finally:
            self.PSQL.cursor.close()

    # Modify the password of a user
    def alter_password(self, data):
        try:
            result_psw = self.take_pass(data['nick_name'])
            verify = self.verify_password_database(
                result_psw, data['password'])

            if verify == False:
                return f'[X] PASSWORD NOT EQUAL!'
            new_pass = self.encript_password(data['new_password'])

            query_update = 'UPDATE users SET password=%s, updated_at=%s WHERE nick_name=%s'
            vars_query = (new_pass, self.date_time_formate, data['nick_name'])
            self.PSQL.cursor.execute(query_update, vars_query)
            self.PSQL.connection.commit()
            row_count = self.PSQL.cursor.rowcount

            print('[✓] UPDADE PASSWORD DONE SUCCESSFULLY IN POSTGRES!')
            return {'Altered Lines': row_count, "Password": 'Update password successfully!'}
        except Exception as error:
            print(error)
            return f'[X] ERROR IN UPDATED USER PASSWORD INFORMATION IN POSTGRES! {error}'
        finally:
            self.PSQL.cursor.close()

    # Show all user of batabase
    def show_all_user(self):
        try:
            sql_select_query = 'SELECT * FROM users'
            self.PSQL.cursor.execute(sql_select_query)
            record = self.PSQL.cursor.fetchall()
            self.PSQL.connection.commit()

            dict_all_users = []
            for index in range(len(record)):
                dict_response = {
                    'nick_name': record[index][1],
                    'name': record[index][3],
                    'email': record[index][5],
                    'phone_number': record[index][6],
                    'created_at': str(record[index][7]),
                    'updated_at': str(record[index][8])

                }
                dict_all_users.append(dict_response)

            print('[✓] SELECT DONE SUCCESSFULLY IN POSTGRES!')
            return dict_all_users
        except Exception as error:
            print(error)
            return f'[X] ERROR ON SELECT IN POSTGRES! {error}'
        finally:
            self.PSQL.cursor.close()

    # Show a user of database
    def show_one_user(self, data):
        try:
            sql_select_query = 'SELECT * FROM users WHERE nick_name=%s'
            vars_query_select = data['nick_name']
            self.PSQL.cursor.execute(sql_select_query, (vars_query_select,))
            record = self.PSQL.cursor.fetchone()
            dict_response = {
                'nick_name': record[1],
                'name': record[3],
                'email': record[5],
                'phone_number': record[6],
                'created_at': str(record[7]),
                'updated_at': str(record[8])
            }

            print('[✓] SELECT DONE SUCCESSFULLY IN POSTGRES!')
            return dict_response
        except Exception as error:
            print(error)
            return f'[X] ERROR ON SELECT IN POSTGRES! {error}'
        finally:
            self.PSQL.cursor.close()

    # Delete a user on database
    def delete_user(self, data):
        try:
            result_psw = self.take_pass(data['nick_name'])
            verify = self.verify_password_database(
                result_psw, data['password'])

            if verify == False:
                return f'[X] PASSWORD NOT EQUAL!'

            sql_delete_query = 'DELETE FROM users WHERE nick_name=%s'
            vars_query_select = data['nick_name']
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

    # get all user's informations on database
    def information_user(self, data):
        try:
            sql_select_query = 'SELECT * FROM users WHERE nick_name=%s'
            vars_query_select = data
            self.PSQL.cursor.execute(sql_select_query, (vars_query_select,))
            record = self.PSQL.cursor.fetchone()
            return record
        except Exception as error:
            print(error)
            return f'[X] ERROR ON SELECT ALL_USER IN POSTGRES! \
        {error}'
        finally:
            self.PSQL.cursor.close()

    # get the user's password
    def take_pass(self, data):
        try:
            sql_select_query = 'SELECT password FROM users WHERE nick_name=%s'
            vars_query_select = data
            self.PSQL.cursor.execute(sql_select_query, (vars_query_select,))
            record = self.PSQL.cursor.fetchone()

            return record
        except Exception as error:
            print(error)
            return f'[X] ERROR SELECT PASSWORD! {error}'

    # Checks input user password with built-in user password
    def verify_password_database(self, db_password, new_pass):
        try:
            EP = EncriptPassword()
            EP.set_pass(new_pass)
            EP.set_hash_pass(db_password[0])
            response_verify = EP.verify_hash()

            if response_verify is True:
                return True
            return False
        except Exception as error:
            print(error)

    # encrypt the user's password
    def encript_password(self, data):
        try:
            HS = EncriptPassword()
            HS.set_pass(data)
            HS.hash_password()
            return HS.get_hash_pass()
        except Exception as error:
            print(error)
            return f'[X] ERROR ON INCRIPTED PASSWORD! \
        {error}'
