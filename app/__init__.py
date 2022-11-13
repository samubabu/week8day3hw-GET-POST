# Import the Flask Class from the flask module
from flask import Flask
# Import SQLAlchemy and Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# import the Config class from the config module
from config import Config


# Create an instance of the Flask class - central object of the whole app
app = Flask(__name__)
# Configure the app using the Config class and the .from_object() method
app.config.from_object(Config)

# Create an instance of SQLAlchemy to represent our database
db = SQLAlchemy(app)
# Create an instance of Migrate to represent our migration engine
migrate = Migrate(app, db)
# Create an instance of LoginManager to let our app allow login capabilities
login = LoginManager(app)
login.login_view = 'login'
login.login_message_category = 'danger'

# Import the api blueprint and register it with the Flask Application 
from app.blueprints.api import api
app.register_blueprint(api)

# import all of the routes and models from the routes and models module in the current folder
from .import routes, models
