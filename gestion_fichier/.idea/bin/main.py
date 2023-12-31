import os
import sqlite3
import logging
from functools import wraps

from flask              import Flask, render_template,g,request,jsonify
from flask_sqlalchemy   import SQLAlchemy
from sqlalchemy.orm     import DeclarativeBase


from init_database      import db,GenericModel
from fileDB             import File
from JwtManager         import encodeToken

__prg_version__ = "0.0.1"
__prg_name__ = "chat"

CHAT_PORT = 5001
CHAT_HOST = "0.0.0.0"
CHAT_DEBUG = True

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["VERSION"] = __prg_version__
app.config["APP_PORT"] = CHAT_PORT
app.config["APP_HOST"] = CHAT_HOST
app.config["APP_DEBUG"] = CHAT_DEBUG
app.config['APP_NAME'] = "Chat :)"
app.config['SECRET_KEY'] = "coucou"


db.init_app(app)


# Db sqlite
DATABASE = 'database.db'
def get_db():
    db = getattr(g, '_database', None);
    if db is not None:
        db.open();

def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(token)
        if not token:
            return jsonify({'message':'Missing or empty token'}),403
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
        except:
            return jsonify({'message':'Invalid token'}),403
        return func(*args,**kwargs)
    return wrapped

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/findFileById/<int:id>", methods=["GET"])
@check_for_token
def findFile(id):
    return db.get_or_404(File, request.view_args['id']).to_dict()

@app.route("/addFile", methods=["POST"])
@check_for_token
def addFileInDataBase():
    if (request.headers.get('Content-Type') == 'application/json'):
        json = request.json
        file = File(json.get('name'),json.get('userName'),json.get('idConversation'),json.get('fileContent'))
        file.save()
        return {'id':file.id},200
    else:
        return 'Content-Type not supported!', 400

def create_app():
    with app.app_context():
        get_db()
        for bp in app.blueprints:
            if 'init_db' in dir(app.blueprints[bp]):
                app.blueprints[bp].init_db()
    app.logger.setLevel(logging.DEBUG)
    return app

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/getToken",methods=['POST'])
def getToken():
    return encodeToken(request.get_json()['username'],app.config['SECRET_KEY'])


app = create_app()
if __name__ == "__main__":
    app.run(host=CHAT_HOST, port=CHAT_PORT, debug=CHAT_DEBUG)