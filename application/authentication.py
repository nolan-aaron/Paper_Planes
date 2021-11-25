from flask import Blueprint, render_template, flash, redirect, url_for, request
from application.forms import RegistrationForm, LoginForm
from application import db
from application.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

blueprint = Blueprint('authentication', __name__)


@blueprint.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    form = RegistrationForm()

    if form.validate_on_submit():

        # Hash password and create the new user
        password_hash = generate_password_hash(form.password.data)
        user = User(username=form.username.data,
                    email=form.email.data, password=password_hash)

        # Store in the database
        db.session.add(user)
        db.session.commit()

        # Sign in the new user then redirect to the home page
        login_user(user)

        flash(
            f"Account created! You're signed in as @{current_user.username}!", 'success')
        return redirect(url_for('routes.index'))

    return render_template('register.html', title='Sign up', form=form)


@blueprint.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(
                f"You signed in as @{user.username}!", 'success')
            return redirect(next_page) if next_page else redirect(url_for('routes.index'))

        else:
            flash(
                f"Login unsuccessful, please try again.", 'danger')

    return render_template('login.html', title='Sign in', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash(
        f"You've been signed out.", 'success')
    return redirect(url_for('routes.index'))
