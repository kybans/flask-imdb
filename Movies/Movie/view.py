from flask import Blueprint,g,request
from migrate import Movie,MovieGenre
from appholder import *
import json
import hashlib
import datetime
from sqlalchemy import func
import requests
from URL_CONSTANTS import API_ROOT
# from User.util import authenticate,get_user_roles
from sqlalchemy.orm import Bundle

movie_blueprint= Blueprint('movie', __name__)



@movie_blueprint.route('/movies',methods=['GET', 'POST','PUT','DELETE'])
def movies():
    # call the service for the authenitcation
    session_id = request.values.get('session_id')
    if not session_id:
        return  json.dumps({'error':'PLS_PROVIDE_SESSION_FOR_AUTHICATION',
                    'status':0})
    role_name = 'user'
    resp = requests.get(API_ROOT + '/user/authenticate?session_id='+session_id)
    if resp.status_code == 200:
        resp = resp.json()
        if not resp or not isinstance(resp,dict) or ('error' in resp or resp.get('status')==0):
            return  json.dumps({'error':'AUTHENTICATION_FAILED',
                    'status':0})
        if 'data' in resp and resp.get('status')==1 and isinstance(resp['data'],list) and len(resp['data']):
            check_role = resp.get('data')[0]
            if isinstance(check_role,dict):
                role_name = check_role.get('role_name').lower()        
            else:
                return  json.dumps({'error':'AUTHENTICATION_FAILED',
                    'status':0})
        else:
            return  json.dumps({'error':'AUTHENTICATION_FAILED',
                    'status':0})
    else:
        return  json.dumps({'error':'AUTHENTICATION_FAILED_INTERNAL_ERROR_OCUURED',
            'status':0})
    
    if request.method == 'POST': 
        try:
            if role_name == 'user':
                return  json.dumps({'error':'NOT_AUTHORISED_CONTACT_ADMIN',
                    'status':0}) 

            movie_name = request.values.get('movie_name')
            if not movie_name:
                return json.dumps({'error':'PLS_PROVIDE_MOVIE_NAME',
                    'status':0})
            director_name = request.values.get('director_name')
            if not director_name:
                return json.dumps({'error':'PLS_PROVIDE_DIRECTOR_NAME',
                    'status':0})
            imdb_score=request.values.get('imdb_score')
            if not imdb_score:
                return json.dumps({'error':'PLS_PROVIDE_imdb_score',
                    'status':0})
            popularity = request.values.get('popularity')
            if not popularity:
                return json.dumps({'error':'PLS_PROVIDE_POPULARITY_FOR_MOVIE',
                    'status':0})

            
            q = Movie(movie_name=movie_name,director_name=director_name,imdb_score=imdb_score,
                popularity =popularity,
                status='A'
            			)
            db.session.add(q)
            db.session.commit()
            return json.dumps({'status':1,'message':'Movie Inserted Successfully!'})
        except Exception as e:
            print "==Something went wrong==",str(e)
            return json.dumps({'error':'CANNOT_CREATE_GENRE_CHECK_LOG','status':0})

    elif request.method == 'GET':
    	try:
            movie_name = request.values.get('movie_name')
            director_name = request.values.get('director_name')
            from_imdb_score=request.values.get('from_imdb_score')
            to_imdb_score=request.values.get('to_imdb_score')
            from_popularity = request.values.get('from_popularity')
            to_popularity = request.values.get('from_popularity')
            movie_id = request.values.get('movie_id')
            genre = request.values.get('genre')
            search_text = request.values.get('search_text')
            #this is also be search functionality
            q = db.session.query(Movie.movie_name,Movie.director_name,Movie.imdb_score,Movie.popularity.label('99popularity'),
                )
            q = q.filter(Movie.status == 'A')
            if movie_name:
                q = q.filter(Movie.movie_name.like(movie_name))
            if movie_id:
                q = q.filter(Movie.id ==movie_id)
            if from_imdb_score:
                q = q.filter(Movie.imdb_score <= from_imdb_score)
            if director_name:
                q = q.filter(Movie.director_name.like(director_name))
            if to_imdb_score:
                q = q.filter(Movie.imdb_score >= to_imdb_score)
            if from_popularity:
                q = q.filter(Movie.popularity <= from_popularity)
            if to_popularity:
                q = q.filter(Movie.popularity >= to_popularity)
            if search_text:
                search_text = ('%' + search_text + '%').lower()
                q = q.filter(or_(func.lower(Movie.name).like(search_text),
                                 func.lower(Movie.director_name).like(search_text)))
            result_set = [u._asdict() for u in q.all()]
            print"==resultset==",result_set
            return json.dumps({'status':1,'data':result_set})
    	except Exception as e:
    		print"==Something went wrong in getting all detials for Genre==",str(e)
    		return json.dumps({'status':0,'error':'CANNOT_FETCH_DATA_FOR_MOVIE'})

    elif request.method == 'PUT':
    	try:
            if role_name == 'user':
                return  json.dumps({'error':'NOT_AUTHORISED_CONTACT_ADMIN',
                    'status':0}) 
            
    		# to update we need genre id
    		movie_name = request.values.get('movie_name')
            if not movie_name:
                return json.dumps({'error':'PLS_PROVIDE_MOVIE_NAME',
                    'status':0})
            director_name = request.values.get('director_name')
            if not director_name:
                return json.dumps({'error':'PLS_PROVIDE_DIRECTOR_NAME',
                    'status':0})
            imdb_score=request.values.get('imdb_score')
            if not imdb_score:
                return json.dumps({'error':'PLS_PROVIDE_imdb_score',
                    'status':0})
            popularity = request.values.get('popularity')
            if not popularity:
                return json.dumps({'error':'PLS_PROVIDE_POPULARITY_FOR_MOVIE',
                    'status':0})
    		movie_id = request.values.get('movie_id')
    		if (not movie_id or movie_id == 'NA' or movie_id is None) or (not movie_id or movie_id == 'NA' or movie_id is None):
    			return json.dumps({'error':'PLS_PROVIDE_MOVIE_ID_AND_MOVIE_NAME_THAT_NEED_TO_BE_EDITED',
    				'status':0})
    		try:
    			#ensure that movie id integer
    			if not isinstance(eval(movie_id),int):
    				return json.dumps({'error':'PLS_PROVIDE_MOVIE_ID_IN_PROPER_FORMAT','status':0})	
    		except Exception as e:
    			print"movie_id not in proper format==",str(e)
    			return json.dumps({'error':'PLS_PROVIDE_GENRE_ID_IN_PROPER_FORMAT','status':0})
    		movie_id= int(movie_id)
    		q = db.session.query(Movie)
    		q.filter(Movie.id == movie_id).update({
    				'movie_name':movie_name,
    				'update_dttm': datetime.datetime.now(),
                    'director_name':director_name,
                    'imdb_score':imdb_score,
                    'popularity':popularity,

  	  			})
    		db.session.commit()	

    		return json.dumps({'status':1,'message':'Genre Updated Successfully!'})
    	except Exception as e:
    		print"==Something went wrong in getting all detials for genre==",str(e)
    		return json.dumps({'status':0,'error':'CANNOT_UPDATING_DATA_FOR_GENRE'})


    elif request.method == 'DELETE':
    	try:
            if role_name == 'user':
                return  json.dumps({'error':'NOT_AUTHORISED_CONTACT_ADMIN',
                    'status':0}) 
            
    		# to DELETE we need movie_id
    		# we will do soft delete
    		movie_id = request.values.get('movie_id')
    		if (not movie_id or movie_id == 'NA' or movie_id is None) :
    			return json.dumps({'error':'PLS_PROVIDE_MOVIE_ID_THAT_NEED_TO_BE_DELETED',
    				'status':0})
    		try:
    			#ensure that movie_id is integer
    			if not isinstance(eval(movie_id),int):
    				return json.dumps({'error':'PLS_PROVIDE_GENRE_ID_IN_PROPER_FORMAT','status':0})	
    		except Exception as e:
    			print"genre_id not in proper format==",str(e)
    			return json.dumps({'error':'PLS_PROVIDE_GENRE_ID_IN_PROPER_FORMAT','status':0})
    		movie_id = int(movie_id)
    		q = db.session.query(Genre)
    		q.filter(Movie.id == movie_id).update({
    				'status':'D',
    				'update_dttm': datetime.datetime.now()

  	  			})
    		db.session.commit()	

    		return json.dumps({'status':1,'message':'Movie Deleted Successfully!'})
    	except Exception as e:
    		print"==Something went wrong in getting all detials for movie==",str(e)
    		return json.dumps({'status':0,'error':'CANNOT_DELETING_DATA_FOR_MOVIE'})
    else:
        return json.dumps({'error':'UNAUTHORISED_METHOD_FOR_ACCESS','status':0})