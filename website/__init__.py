from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)

    from .views import my_view
    app.register_blueprint(my_view)

    from .models import Todo
    with app.app_context():
        db.create_all()

    return app

#! The create_app function sets up and configures the Flask app.
#! Creates a Flask app instance and configures it to use the SQLite database.
#! Initialises the SQLAlchemy instance with the app.
#! Imports and registers a blueprint for organising the application.
#! It imports the Todo model and creates the necessary database tables within the app.
#! It will then return the configured Flask app.