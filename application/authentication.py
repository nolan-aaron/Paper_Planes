from flask import Blueprint, render_template, flash, redirect, url_for
from application.forms import RegistrationForm, LoginForm

blueprint = Blueprint('authentication', __name__)


@blueprint.route("/register", methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        flash(
            f"Account created for @{form.username.data}! Please sign in below.", 'success')
        return redirect(url_for('authentication.login'))

    return render_template('register.html', title='Sign up', form=form)


@blueprint.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == 'nolan_aaron@outlook.com' and form.password.data == '12345678':
            flash(f"You have been logged in!", 'success')
            return redirect(url_for('routes.index'))
        else:
            flash(f"Login unsuccessful, please check your email and password.", 'danger')

    return render_template('login.html', title='Sign in', form=form)
