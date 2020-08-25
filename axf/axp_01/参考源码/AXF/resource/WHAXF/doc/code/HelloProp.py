

class User:

    u_name = ''

    _password = ''

    @property
    def u_password(self):
        return self._password

    @u_password.setter
    def u_password(self, pwd):
        self._password = pwd




if __name__ == '__main__':
    u = User()

    u.u_password = '110'

    # print(u._password)

    print(u.u_password)
