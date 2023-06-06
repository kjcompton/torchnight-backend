from flask import Flask, jsonify, g
from flask_cors import CORS

import models
from resources.users import users

app = Flask(__name__)

CORS(users, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(users, url_prefix='/api/v1/users')


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


# Run app when it starts
if __name__ == '__main__':
    # when we start the app, set up our DB/tables as defined in models.py
    models.initialize()
    app.run(debug=True, port=8000)