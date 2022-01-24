from flask import Blueprint, render_template, flash, redirect, url_for, request
from application.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from application import db, create_app
from application.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from flask_mail import Mail
from datetime import datetime
import time
import pytz
from ipstack import GeoLookup
import os
from requests import get
import socket

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
            f"You're in! Feel free to change your profile photo below, or keep the one we've given you.", 'success')

        return redirect(url_for('profile.profile'))

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
            return redirect(next_page) if next_page else redirect(url_for('routes.index'))

        else:
            flash(
                f"Log in unsuccessful, please try again.", 'danger')

    return render_template('login.html', title='Log in', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))


def send_reset_email(user, user_agent, formatted_datetime, user_location):
    token = user.get_reset_token()
    msg = Message('Password Reset',
                  sender='paper-planes.herokuapp@outlook.com',
                  recipients=[user.email])
    msg.html = f'''<p>Hi @{user.username},</p>

<p>We received a request to reset the password for your Paper Planes account. You can click the button below to reset it.</p>

<a href="{url_for('authentication.reset_token', token=token, _external=True)}"><button style="background-color: #3f3fff; color: white; padding: 10px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: bold">Reset your password</button></a><br>

<small>Note: this link is only valid for 24 hours.</small>

<p><b>Device:</b> {user_agent.platform} ({user_agent.browser})<br>
<b>Location:</b> {user_location}<br>
<b>Date:</b> {formatted_datetime}</p>

<p>If you did not request a new password, you can safely ignore this email or <a href="mailto:paper-planes.herokuapp@outlook.com">contact us</a> for support.</p>

<p>— The Paper Planes team</p>
'''
    mail = Mail(create_app())
    mail.send(msg)


@blueprint.route("/reset_password", methods=['GET', 'POST'])
def reset_request():

    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    # GET USER_AGENT (DEVICE/BROWSER)
    user_agent = request.user_agent
    tz_Aus = pytz.timezone('Australia/Brisbane')
    datetime_Aus = datetime.now(tz_Aus)
    formatted_datetime = datetime_Aus.strftime('%B %d at %-I:%M %p')

    # CONNECT TO IPSTACK API
    ACCESS_KEY = '0ebf65cf0f5e120095e3d33dd7c859dc'
    geo_lookup = GeoLookup(ACCESS_KEY)

    # GET USER IP ADDRESS --> FIX THIS, NOT ABLE TO PULL CORRECT IP
    # ip_address = get('https://api.ipify.org').text
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # GET CITY/REGION DATA BASED ON IP ADDRESS
    location = geo_lookup.get_location(ip_address)
    city = location['city']
    region = location['region_name']

    # IF NOT ABLE TO LOCATE CITY/REGION DATA
    if city is None or region is None:
        user_location = 'Not available'

    else:
        user_location = f'{city}, {region}'

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # Send password reset if an account exists for the provided email
        if user:
            send_reset_email(user, user_agent,
                             formatted_datetime, user_location)

        # Simulate delay of sending an email to prevent enumeration attacks
        else:
            time.sleep(4)

        flash('If an account exists for this email, we will shortly send a link to reset the password', 'info')
        return redirect(url_for('authentication.login'))

    return render_template('reset_request.html', title='Reset password', form=form)


@blueprint.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):

    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    user = User.verify_reset_token(token)

    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('authentication.reset_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():

        # Hash password and create the new user
        password_hash = generate_password_hash(form.password.data)

        # Store in the database
        user.password = password_hash
        db.session.commit()

        flash(
            f"Your password has been updated! Please log in below.", 'success')

        return redirect(url_for('authentication.login'))

    return render_template('reset_token.html', title='Set new password', form=form)
