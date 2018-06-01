from flask import Blueprint,g,request
from migrate import Role,User,UserLogin
from appholder import *
import json
import hashlib
from util import generate_password_hash,generate_session,authenticate,get_user_roles
import uuid
from flask import Response
user_blueprint= Blueprint('user', __name__)



@user_blueprint.route('/user/register',methods=['POST'])
def user_register():
    if request.method == 'POST': 
        try:
            user_name = request.values.get('user_name')
            password = request.values.get('password')
            role_id = request.values.get('role_id')
            if not user_name:
                return json.dumps({'error':'user_name_IS_MANDOTRY','status':0})
            if not password:
                return json.dumps({'error':'password_IS_MANDOTRY','status':0})
            else:
                #check length for password
                pass_length = len(password)
                if pass_length < 3 or pass_length > 10:
                    return json.dumps({'error':'PASSWORD_SHOULD_BE_BETWEEN_LENGTH_3_TO_10','status':0})
            if not role_id:
                return json.dumps({'error':'role_id_IS_MANDOTRY','status':0})

            l = User.query.filter_by(user_name=user_name).one_or_none()
            if l is None:
                #hash the password and then store
                encrypted_pass = generate_password_hash(password = password)
                if isinstance(encrypted_pass,bool):
                    return json.dumps({'error':'SOMETHING_WENT_WRONG_IN_STORING_DATA_WHILE REGISTER','status':0})
                user_uuid = uuid.uuid4()
                l = User(user_name=user_name, password=encrypted_pass, role_id=role_id,status='A',uuid=str(user_uuid))
            else:
                return json.dumps({'errors': 'USERNAME_ALREADY_EXISTS', 'status': 0})
            db.session.add(l)
            db.session.commit()
            # create entry in the session
            # and make user login
            # store session/token in the cookies
            session_id = generate_session(uuid=user_uuid)
            if isinstance(session_id,bool):
                return json.dumps({'error':'SOMETHING_WENT_WRONG_IN_LOGGING_USER','status':0})
            js={'status':1,'message':'login_created'}
            resp = Response(js, status=200, mimetype='application/json')
            resp.set_cookie('session_id', session_id.session_id, expires=session_id.expiration_ttm)
            return resp

        except Exception as e:
            print "==Something went wrong==",str(e)
            return json.dumps({'error':'SOMETHING_WENT_WRONG_IN_LOGGING_USER','status':0})

    else:
        return json.dumps({'error':'UNAUTHORISED_METHOD_FOR_ACCESS','status':0})


@user_blueprint.route('/user/login',methods=['POST'])
def user_login():
    if request.method == 'POST': 
        try:
            user_name = request.values.get('user_name')
            password = request.values.get('password')

            if not user_name:
                return json.dumps({'error':'user_name_IS_MANDOTRY','status':0})
            if not password:
                return json.dumps({'error':'password_IS_MANDOTRY','status':0})
            # check that user_name exits or not
            l = User.query.filter_by(user_name=user_name).one_or_none()
            if l is None:
                return json.dumps({'error':'USER_IS_NOT_REGISTERED','status':0})
            #authenticate password
            exsisting_password = l.password
            if not exsisting_password == generate_password_hash(password):
                return json.dumps({'error':'PASSWORD_IS_INVALID','status':0})
            # check the seesion and if there is active session deactivate them
            session_id = request.cookies.get('session_id')
            if session_id:
                session_auth = authenticate(session_id=session_id)
                if session_auth:
                    db.session.query(UserLogin).filter(UserLogin.session_id == session_id).update({
                        'status':'D'
                        })
            # create new seesion for login
            session_id = generate_session(uuid=l.uuid)
            if isinstance(session_id,bool):
                return json.dumps({'error':'SOMETHING_WENT_WRONG_IN_LOGGING_USER','status':0})
            js={'status':1,'message':'login_created'}
            resp = Response(js, status=200, mimetype='application/json')
            resp.set_cookie('session_id', session_id.session_id, expires=session_id.expiration_ttm)
            return resp


            

        except Exception as e:
            print "==Something went wrong==",str(e)
            return json.dumps({'error':'SOMETHING_WENT_WRONG_IN_LOGGING_USER','status':0})

    else:
        return json.dumps({'error':'UNAUTHORISED_METHOD_FOR_ACCESS','status':0})



@user_blueprint.route('/user/logout',methods=['GET'])
def user_logout():
    if request.method == 'GET': 
        try:
            session_id = request.values.get('session_id')
            # check the seesion and if there is active session deactivate them
            if not session_id:
                session_id = request.cookies.get('session_id')
            if session_id:
                db.session.query(UserLogin).filter(UserLogin.session_id == session_id).update({
                    'status':'D'
                    })

            return json.dumps({'status':1,'message':'Logged Out Successfully!'})

            

        except Exception as e:
            print "==Something went wrong==",str(e)
            return json.dumps({'error':'SOMETHING_WENT_WRONG_IN_LOGGING_OUT_USER','status':0})

    else:
        return json.dumps({'error':'UNAUTHORISED_METHOD_FOR_ACCESS','status':0})

@user_blueprint.route('/user/authenticate',methods=['GET'])
def user_authenticate():
    if request.method == 'GET': 
        try:
            roles_data ={}
            session_id = request.values.get('session_id')
            print"===what is seesion==",session_id
            # check the seesion and if there is active session deactivate them
            if not session_id:
                session_id = request.cookies.get('session_id')
            if session_id:
                session_auth = authenticate(session_id=session_id)
                print"====check user_is authenicated====session is on==",session_auth
                ## if session is authorised we will check for the roles
                roles_data = get_user_roles(session_id=session_id)
            return json.dumps({'status':1,'message':'Roles Data','data':roles_data})

        except Exception as e:
            print "==Something went wrong==",str(e)
            return json.dumps({'error':'SOMETHING_WENT_WRONG_IN_LOGGING_OUT_USER','status':0})

    else:
        return json.dumps({'error':'UNAUTHORISED_METHOD_FOR_ACCESS','status':0})


    