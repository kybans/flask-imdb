from appholder import *
from Genre.view import genre_blueprint
from Movie.view import movie_blueprint
from flask import g
import json

app.register_blueprint(genre_blueprint)
app.register_blueprint(movie_blueprint)

@app.before_request
def before_request():
    # g.user = current_user

    g.con = mysql.connect()




if __name__ == '__main__':
   app.run(debug=True,port=5001)