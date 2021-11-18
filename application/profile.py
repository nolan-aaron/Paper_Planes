from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint('profile', __name__, url_prefix='/profile')


@blueprint.route("/")
@login_required
def profile():
    return render_template('profile.html')
