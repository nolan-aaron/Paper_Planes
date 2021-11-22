from flask import Blueprint, render_template
from application.models import Post
from datetime import datetime, time, timezone

blueprint = Blueprint('routes', __name__)


@blueprint.route("/")
def index():

    posts = Post.query.order_by(Post.date_posted.desc()).all()

    return render_template('index.html', posts=posts, elapsed_time=elapsed_time)


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
