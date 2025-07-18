from flask import Flask
from applications.database import db #step_3: database
import os


app = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.sqlite3" #step_3: database
    db.init_app(app) #step_3: database
    app.app_context().push() #otherwise gives runtime error, it brings everything under the context of flask application, Direct access to other modules
    return app

app = create_app()
from applications.controllers import * #step_2: controllers
# from applications.models import * #connected indirectly through controllers.py

app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

if __name__ == '__main__':
    app.run()    