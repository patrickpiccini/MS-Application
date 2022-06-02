
from argon2 import PasswordHasher

## encapsulamento
class EncriptPassword():

    def __init__(self):
        self.ph = PasswordHasher()
        self.__password = ''
        self.__hash_password = ''

    #password
    def get_pass(self):
        return self.__password
    
    def set_pass(self, password_imput):
        self.__password = password_imput

    #hash password
    def get_hash_pass(self):
        return self.__hash_password
    
    def set_hash_pass(self, hash_pass):
        self.__hash_password = hash_pass
    
    def hash_password(self):
        self.__hash_password = self.ph.hash(self.__password)

    def verify_hash(self):
        try:
            return self.ph.verify(self.__hash_password, self.__password)
        except Exception as error:
            print('Erro in verify hash',error)
            return False


if __name__ == '__main__':
    ec = EncriptPassword()
    ec.set_pass("Senha@¨123")
    ec.hash_password()
    print(ec.verify_hash())
    # print(ec.get_pass())




    