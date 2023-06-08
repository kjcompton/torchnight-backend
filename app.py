from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv
from resources.users import users
from resources.characters import characters

import models
import os

load_dotenv()

login_manager = LoginManager()

app = Flask(__name__)

app.secret_key = os.environ.get("APP_SECRET")

login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except:
        return None


@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response

# Health Check
@app.route('/')
def index():
    return 'Server is running'


CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(users, url_prefix='/api/v1/users')

CORS(characters, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(characters, url_prefix='/api/v1/characters')


# Run app when it starts
if __name__ == '__main__':
    # when we start the app, set up our DB/tables as defined in models.py
    models.initialize()
    app.run(debug=True, port=8000)