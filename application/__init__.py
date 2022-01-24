import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()


def create_app():

    # Create and configure the application
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'd8406b95c0ef1a9fe9daefdbdd720bad70ac3977d3abf8db667a4e6f1be24cc7'

    # SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)

    # Mail settings
    app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    # os.environ.get('EMAIL_USER')
    app.config['MAIL_USERNAME'] = 'paper-planes.herokuapp@outlook.com'
    # os.environ.get('EMAIL_PASS')
    app.config['MAIL_PASSWORD'] = 'Wd3Ltqt3wWxk8ReV'
    mail = Mail(app)

    # Configure the login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'authentication.login'
    login_manager.login_message = 'You need to sign in before you can do that!'
    login_manager.login_message_category = 'info'

    from application.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import routes module to avoid circular references
    from application import routes
    app.register_blueprint(routes.blueprint)

    # Import authentication module to avoid circular references
    from application import authentication
    app.register_blueprint(authentication.blueprint)

    # Import account module to avoid circular references
    from application import profile
    app.register_blueprint(profile.blueprint)

    # Import post module to avoid circular references
    from application import post
    app.register_blueprint(post.blueprint)

    return app
