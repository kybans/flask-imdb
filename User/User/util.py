import hashlib
import random
from flask import request as req
import time
import pytz
from pytz import timezone
from datetime import datetime, timedelta,date
from flask import Response
from migrate import UserLogin,User,Role
from appholder import *
def generate_password_hash(password=False):
    """
    this function will generate the password hash that we can store in the database,and also
    then we use the same for authentication.
    @params:password:this is mandotry param its basically the raw password
    """
    if not password:
        return False
    unique = 'onionkandalogin'
    key = hashlib.sha256(password + unique).hexdigest()
    return key

def generate_session(uuid=False):
    """
    this function will generate the login session for the
    current user we will store the user_uuid with session_id
    and its expiration time.default is set to 60 mins,for each
    operations like login,register respectively
    """
    if not uuid:
        return False
    ts = time.time()
    session_id = str(uuid)+str(ts)
    expires = (datetime.utcnow() + timedelta(hours=1)).replace(tzinfo=pytz.utc)
    q = UserLogin(user_token=uuid,session_id=session_id,expiration_ttm=expires)
    db.session.add(q)
    db.session.commit()
    return q

def authenticate(session_id=False):
    """
    this function will authenticate the session and user from the session
    """
    # first check if the session_id is present in cookies
    """
    this method will send False if the session has expired
    :return: 
    """
    if 'session_id' in req.cookies:
        session_id = req.cookies.get('session_id')
    elif session_id:
        session_id=session_id
    else:
        return False
    current_time = datetime.utcnow().replace(tzinfo=pytz.utc)
    print"===="
    print type(current_time)
    print"===="
    current_time = datetime.strptime(datetime.strftime(current_time,'%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
    # localtz = timezone('Asia/Kolkata')
    # current_time = localtz.localize(datetime.now())
    s = UserLogin.query.filter_by(session_id=session_id,status='A').one_or_none()
    print "===check bothhh==", s.expiration_ttm, current_time, s.expiration_ttm < current_time
    if s and s.expiration_ttm < current_time:
        return False
    else:
        return True


def get_user_roles(session_id=False):
    """
    this function will return the role of the user
    """
    if 'session_id' in req.cookies:
        session_id = req.cookies.get('session_id')
    elif session_id:
        session_id=session_id
    else:
        return False
    q = db.session.query(UserLogin.user_token,Role.role_name.label('role_name'))
    q = q.join(User,UserLogin.user_token == User.uuid)
    q = q.join(Role,User.role_id == Role.id)
    q = q.filter(User.status == 'A')
    q = q.filter(Role.status == 'A')
    q = q.filter(UserLogin.status == 'A')
    q = q.filter(UserLogin.session_id == session_id)
    result_set = [u._asdict() for u in q.all()]
    return result_set

    
