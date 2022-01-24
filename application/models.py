from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from application import db, create_app
from datetime import datetime
from flask_login import UserMixin

# CREATE NEW DATABASE

# python3
# from application import db, create_app
# app=create_app()
# ctx=app.app_context()
# ctx.push()
# db.create_all() or db.drop_all()
# quit()


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(8), unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_secs=86400):

        app = create_app()
        s = Serializer(app.config['SECRET_KEY'], expires_secs)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):

        app = create_app()
        s = Serializer(app.config['SECRET_KEY'])

        try:
            user_id = s.loads(token)['user_id']

        except:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(300), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    edited = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.content}', '{self.date_posted}')"
