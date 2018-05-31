from flask import Blueprint,g,request
from migrate import Movie,MovieGenre
from appholder import *
import json
import hashlib
import datetime
from sqlalchemy import func
from User.util import authenticate,get_user_roles
from sqlalchemy.orm import Bundle

movie_blueprint= Blueprint('movie', __name__)



@movie_blueprint.route('/movies',methods=['GET', 'POST','PUT','DELETE'])
def movie():
    if not authenticate():
        return json.dumps({'status':0,'error':'SESSION_IS_INVALID_PLEASE_LOGIN_AGAIN!'})
    
    if request.method == 'POST': 
        try:
            if get_user_roles():
                roles_detail = get_user_roles()
                if roles_detail and roles_detail[0].get('roles_detail').lower()=='user':
                    return json.dumps({'status':0,'error':'USER_NOT_AUTHORISED_CONTACT_ADMIN!'})

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
                popularity =popularity
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
            movie_id = request.vales.get('movie_id')
            genre = request.values.get('genre')
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
    		result_set = [u._asdict() for u in q.all()]
    		return json.dumps({'status':1,'data':result_set})
    	except Exception as e:
    		print"==Something went wrong in getting all detials for Genre==",str(e)
    		return json.dumps({'status':0,'error':'CANNOT_FETCH_DATA_FOR_GENRE'})

    elif request.method == 'PUT':
    	try:
            if get_user_roles():
                roles_detail = get_user_roles()
                if roles_detail and roles_detail[0].get('roles_detail').lower()=='user':
                    return json.dumps({'status':0,'error':'USER_NOT_AUTHORISED_CONTACT_ADMIN!'})
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
            if get_user_roles():
                roles_detail = get_user_roles()
                if roles_detail and roles_detail[0].get('roles_detail').lower()=='user':
                    return json.dumps({'status':0,'error':'USER_NOT_AUTHORISED_CONTACT_ADMIN!'})
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