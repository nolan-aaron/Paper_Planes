from flask import render_template, flash, redirect, url_for, Blueprint
from application import create_app
from application.forms import RegistrationForm, LoginForm
from application.models import User, Post

blueprint = Blueprint('routes', __name__)

posts = [
    {
        'username': '@aaron_nolan',
        'content': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae vero ut odio aut. Asperiores amet minus iste nemo ratione atque.',
        'posted': '34 minutes ago'
    },
    {
        'username': '@libby_hogarth',
        'content': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae vero ut odio aut. Asperiores amet minus iste nemo ratione atque.',
        'posted': '7 minutes ago'
    }
]


@blueprint.route("/")
def index():
    return render_template('index.html', posts=posts)
