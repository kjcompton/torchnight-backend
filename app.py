from flask import Flask, jsonify, g, after_this_request
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv
from resources.users import users
from resources.characters import characters

import models
import os

# Test
load_dotenv()

# login_manager = LoginManager()

app = Flask(__name__)

app.secret_key = os.environ.get("APP_SECRET")




@app.before_request
def before_request():
    models.DATABASE.connect()

    @after_this_request
    def after_request(response):
        models.DATABASE.close()
        return response


# Health Check
@app.route('/')
def index():
    return 'Server is running'

CORS(app)
# CORS(users, origins=['http://localhost:5173'], supports_credentials=True)
app.register_blueprint(users, url_prefix='/api/v1/users')

# CORS(characters, origins=['http://localhost:5173'], supports_credentials=True)
app.register_blueprint(characters, url_prefix='/api/v1/characters')


# Run app when it starts
if __name__ == '__main__':
    # when we start the app, set up our DB/tables as defined in models.py
    models.initialize()
    app.run(debug=True, port=8000)

# ADD THESE THREE LINES -- because we need to initialize the
# tables in production too!
if os.environ.get('FLASK_ENV') != 'development':
  print('\non heroku!')
  models.initialize()
