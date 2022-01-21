from flask import Blueprint, render_template, request
from application.models import Post, User
from datetime import datetime

blueprint = Blueprint('routes', __name__)


@blueprint.route("/")
def index():

    # Pagination
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template('index.html', posts=posts, elapsed_time=elapsed_time, total_users=total_users, total_posts=total_posts, latest_user=latest_user)


# Below three functions should be moved to models.py
def total_users():
    return User.query.count()


def total_posts():
    return Post.query.count()


def latest_user():
    return User.query.order_by(User.date_joined.desc()).first().username


def elapsed_time(post):

    seconds = int(datetime.utcnow().strftime('%s')) - \
        int(post.date_posted.strftime('%s'))

    if seconds == 1:
        value = seconds
        unit_of_time = 'second'

    elif seconds < 60:
        value = seconds
        unit_of_time = 'seconds'

    elif seconds < 120:
        value = int(seconds / 60)
        unit_of_time = 'minute'

    elif seconds < 3600:
        value = int(seconds / 60)
        unit_of_time = 'minutes'

    elif seconds < 7200:
        value = int(seconds / 60 / 60)
        unit_of_time = 'hour'

    elif seconds < 86400:
        value = int(seconds / 60 / 60)
        unit_of_time = 'hours'

    elif seconds < 172800:
        value = int(seconds / 60 / 60 / 24)
        unit_of_time = 'day'

    else:  # Implied 2 or more days ago
        value = int(seconds / 60 / 60 / 24)
        unit_of_time = 'days'

    return f'{value} {unit_of_time} ago'


@blueprint.route("/user/<string:username>")
def user_posts(username):

    # Try to locate the user being queried
    user = User.query.filter_by(username=username).first_or_404()

    # Pagination
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template('user_posts.html', posts=posts, user=user, elapsed_time=elapsed_time)
