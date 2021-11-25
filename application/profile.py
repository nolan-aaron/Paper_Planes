import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, url_for, request
from flask.helpers import flash
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from application.forms import UpdateProfileForm
from application import db

blueprint = Blueprint('profile', __name__, url_prefix='/profile')


def save_picture(form_picture):

    # Generate random file name for the image and concatenate with the file extension (jpg or png)
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension

    # Create the image path
    BASE_PATH = os.path.dirname(__file__)
    picture_path = os.path.join(
        BASE_PATH, 'static/profile_pics', picture_filename)

    # Resize image
    image_size = (400, 400)
    image = Image.open(form_picture)
    image.thumbnail(image_size)

    # Save the image path
    image.save(picture_path)

    return picture_filename


@blueprint.route("/", methods=['GET', 'POST'])
@login_required
def profile():

    form = UpdateProfileForm()

    if form.validate_on_submit():

        if form.picture.data:

            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"Your profile has been updated!", 'success')

        return redirect(url_for('profile.profile'))

    elif request.method == 'GET':

        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for(
        'static', filename=f'profile_pics/{current_user.image_file}')

    date_joined = current_user.date_joined.strftime('%d %b, %Y')

    return render_template('profile.html', title='Profile', image_file=image_file, form=form, date_joined=date_joined)
