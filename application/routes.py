from flask import Blueprint, render_template

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
