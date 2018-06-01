from appholder import *
# from Movies.views import movies_blueprint


from sqlalchemy import Column, DateTime, Integer, String, text,Float





    

class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, name='id')
    user_name = Column(String(10), name='user_name')
    password = Column(String(500), name='password')
    role_id = Column(Integer,db.ForeignKey('role.id'))
    uuid = Column(String(50),name='uuid')
    update_dttm = Column(DateTime(True), server_default=text("now()"), name='update_dttm')
    create_dttm = Column(DateTime(True), server_default=text("now()"), name='create_dttm')
    status = Column(String(1), name='status', default='A')

class Role(db.Model):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, name='id')
    role_name = Column(String(12), name='role_name')
    update_dttm = Column(DateTime(True), server_default=text("now()"), name='update_dttm')
    create_dttm = Column(DateTime(True), server_default=text("now()"), name='create_dttm')
    status = Column(String(1), name='status', default='A')


class UserLogin(db.Model):
    __tablename__ = 'user_login'

    id = Column(Integer, primary_key=True, name='id')
    user_token = Column(String(100),name='user_token')
    session_id = Column(String(100),name='session_id')
    expiration_ttm = Column(DateTime(True),name='expiration_ttm')
    update_dttm = Column(DateTime(True), server_default=text("now()"), name='update_dttm')
    create_dttm = Column(DateTime(True), server_default=text("now()"), name='create_dttm')
    status = Column(String(1), name='status', default='A')





if __name__ == '__main__':
   manager.run()