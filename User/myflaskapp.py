from appholder import *
from Role.view import role_blueprint
from User.view import user_blueprint

from flask import g
import json

app.register_blueprint(role_blueprint)
app.register_blueprint(user_blueprint)

@app.before_request
def before_request():
    # g.user = current_user

    g.con = mysql.connect()




if __name__ == '__main__':
   app.run(debug=True,port=5000)