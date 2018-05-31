from flask import Blueprint,g,request
from migrate import Role,User
from appholder import *
import json
import hashlib
import datetime
from sqlalchemy import func
role_blueprint= Blueprint('role', __name__)



@role_blueprint.route('/role',methods=['GET', 'POST','PUT','DELETE'])
def role():
    if request.method == 'POST': 
        try:
            role_name = request.values.get('role_name','user')
            role_name = role_name.lower()
            q = Role(role_name=role_name,status='A'
            			)
            db.session.add(q)
            db.session.commit()
            return json.dumps({'status':1,'message':'Role Inserted Successfully!'})
        except Exception as e:
            print "==Something went wrong==",str(e)
            return json.dumps({'error':'CANNOT_CREATE_ROle_CHECK_LOG','status':0})

    elif request.method == 'GET':
    	try:
    		q = db.session.query(Role.role_name,Role.status)
    		q = q.filter(Role.status == 'A')
    		result_set = [u._asdict() for u in q.all()]
    		return json.dumps({'status':1,'data':result_set})
    	except Exception as e:
    		print"==Something went wrong in getting all detials for roles==",str(e)
    		return json.dumps({'status':0,'error':'CANNOT_FETCH_DATA_FOR_ROLE'})

    elif request.method == 'PUT':
    	try:
    		# to update we need role id
    		role_name = request.values.get('role_name')
    		role_id = request.values.get('role_id')
    		if (not role_id or role_id == 'NA' or role_id is None) or (not role_name or role_name == 'NA' or role_name is None):
    			return json.dumps({'error':'PLS_PROVIDE_ROLE_ID_AND_ROLE_NAME_THAT_NEED_TO_BE_EDITED',
    				'status':0})
    		try:
    			#ensure that role_id is integer
    			if not isinstance(eval(role_id),int):
    				return json.dumps({'error':'PLS_PROVIDE_ROLE_ID_IN_PROPER_FORMAT','status':0})	
    		except Exception as e:
    			print"role_id not in proper format==",str(e)
    			return json.dumps({'error':'PLS_PROVIDE_ROLE_ID_IN_PROPER_FORMAT','status':0})
    		role_id = int(role_id)
    		q = db.session.query(Role)
    		q.filter(Role.id == role_id).update({
    				'role_name':role_name,
    				'update_dttm': datetime.datetime.now()

  	  			})
    		db.session.commit()	

    		return json.dumps({'status':1,'message':'Role Updated Successfully!'})
    	except Exception as e:
    		print"==Something went wrong in getting all detials for roles==",str(e)
    		return json.dumps({'status':0,'error':'CANNOT_UPDATING_DATA_FOR_ROLE'})


    elif request.method == 'DELETE':
    	try:
    		# to DELETE we need role_id
    		# we will do soft delete
    		role_id = request.values.get('role_id')
    		if (not role_id or role_id == 'NA' or role_id is None) :
    			return json.dumps({'error':'PLS_PROVIDE_ROLE_ID_THAT_NEED_TO_BE_DELETED',
    				'status':0})
    		try:
    			#ensure that role_id is integer
    			if not isinstance(eval(role_id),int):
    				return json.dumps({'error':'PLS_PROVIDE_ROLE_ID_IN_PROPER_FORMAT','status':0})	
    		except Exception as e:
    			print"role_id not in proper format==",str(e)
    			return json.dumps({'error':'PLS_PROVIDE_ROLE_ID_IN_PROPER_FORMAT','status':0})
    		role_id = int(role_id)
    		q = db.session.query(Role)
    		q.filter(Role.id == role_id).update({
    				'status':'D',
    				'update_dttm': datetime.datetime.now()

  	  			})
    		db.session.commit()	

    		return json.dumps({'status':1,'message':'Role Deleted Successfully!'})
    	except Exception as e:
    		print"==Something went wrong in getting all detials for roles==",str(e)
    		return json.dumps({'status':0,'error':'CANNOT_DELETING_DATA_FOR_ROLE'})
    else:
        return json.dumps({'error':'UNAUTHORISED_METHOD_FOR_ACCESS','status':0})