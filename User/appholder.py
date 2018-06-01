from flask import Flask, render_template, request
import sqlite3 as sql
from flask import Flask
# from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
import config
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand


app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)
mysql = MySQL()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/imdb'
app.config['MYSQL_DATABASE_USER'] = config.DB_USER
app.config['MYSQL_DATABASE_PASSWORD'] = config.DB_PASSWORD
app.config['MYSQL_DATABASE_DB'] = config.APP_NAME
app.config['MYSQL_DATABASE_HOST'] = config.DB_HOST
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Flask
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)
mysql = MySQL()

mysql.init_app(app)