# flask-imdb

################################

#Introduction flask-imdb:

This Repository contains the basic CRUD operations for model similar to imdb,

it is based on python-flask restfull api framework, for database we have used mysql version 5.0.12,

here we have used two services for flask and divided our 'Movie' logic and 'User' Signup logic separately.

#Database:

We have created two databases 'imdb' and 'imdb_movie' for storing user detials and movie details respectively.

Note: need to ensure that database is created prior,use follwing in cli or mysql query box,
$ create database imdb;
$ create database imdb_movie;

Also, need to ensure that mysql version is properly set for connection;with required connection parameters

host:localhost ['Since our database server and Flask server is same']
user: root ['The database is created under root to ensure it get all needed access']
password :root ['The Password used for this connection to mysql is 'root'].

However, we can use any configuration as per our convenience and requirements.
all we need to do is change in the config.py file for each flask app 'User' and 'Movies' respectively.

#flask-apps:

There are two flask app 'User' and 'Movie' running on port 5000 and 5001 respectively.

for authentication purpose of our Api's, Movie app communicates with User app.

#models:

We have models for:

1.User
2.Movies
3.Genre
4.Roles
5.MovieGenre (Many2Many relationship)
6.UserLogin(To keep track for user that has login with session expiration)

we have METHOD 'GET','POST','PUT','DELETE' for READ,INSERT/CREATE,UPDATE,DELETE  on models respectively.

#flask-database-migration:

For database migration we have used flask-alembic, which creates migrations file in each app
execute following command to run migration for each app:
 
$ python migrate.py db init
if migration file already exists then delete first and then execute command

$ python migrate.py db migrate

$ python migrate.py db upgrade

to set database path for flask-envornment variable use following comand
$ export DATABASE_URL="mysql://root:root@localhost/imdb" for User app
$ export DATABASE_URL="mysql://root:root@localhost/imdb_movie" for Movie app

#flask API's authentication:

All API's in  each app requires valid session, which is stored in response cookies at the time of login and signup

All API's except 'GET' for /movies and /user/login and /user/register it requires admin role access



#Session-Management:

Session for every user is generated at the time of login or signup , it stored in mysql database inside
table user_login, with expiration_time,

to send session_id as the request in parameter we are storing 'session_id' value in cookie


#future-scope to make scalable:

In order to make more scalable we can change the way of our authentication.(currently checking  expiration of session from mysql), we can use session or cache database like redis, which is much reliable for storing session with expiration time.

We Can Make it full Microservice, wherein our Movie app is implemented in Django or any other framework,
which seems to be releiable for seaching and dispalying.

#for any issues email me on : nirmalvyas88@gmail.com



