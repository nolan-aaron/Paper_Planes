from flask import Flask, render_template, flash, redirect
from flask.helpers import url_for
from forms import RegistrationForm, LoginForm

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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd8406b95c0ef1a9fe9daefdbdd720bad70ac3977d3abf8db667a4e6f1be24cc7'


@app.route("/")
def index():
    return render_template('index.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f"Account created for @{form.username.data}!", 'success')
        return redirect(url_for('index'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == 'nolan_aaron@outlook.com' and form.password.data == '12345678':
            flash(f"You have been logged in!", 'success')
            return redirect(url_for('index'))
        else:
            flash(f"Login unsuccessful, please check your email and password.", 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    app.run(debug=True)
