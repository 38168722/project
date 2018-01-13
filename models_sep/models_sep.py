from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Article

app = Flask(__name__)

db = SQLAlchemy(app)
db.create_all()

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
