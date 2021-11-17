from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():

    # Create and configure the application
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'd8406b95c0ef1a9fe9daefdbdd720bad70ac3977d3abf8db667a4e6f1be24cc7'

    # SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)

    # Import routes module to avoid circular references
    from application import routes
    app.register_blueprint(routes.blueprint)

    # Import authentication module to avoid circular references
    from application import authentication
    app.register_blueprint(authentication.blueprint)

    return app
