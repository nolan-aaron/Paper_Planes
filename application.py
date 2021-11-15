from flask import Flask, render_template


app = Flask(__name__)
app.secret_key = 'd8406b95c0ef1a9fe9daefdbdd720bad70ac3977d3abf8db667a4e6f1be24cc7'


@app.route("/")
def index():
    return render_template('base.html')


if __name__ == "__main__":
    app.run(debug=True)
