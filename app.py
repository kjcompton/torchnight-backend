from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    # when we start the app, set up our DB/tables as defined in models.py
    app.run(debug=True, port=8000)