from flask import Flask, Response, redirect, url_for, request, session, abort, render_template
from flask_login import LoginManager, UserMixin, \
    login_required, login_user, logout_user
#from database import db_session
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

# config
app.config.update(
    DEBUG=True,
    SECRET_KEY='ASDADADF566FVF8RVEVE1VE51VVF5',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
 )
# app.config['DEBUG'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

    def __repr__(self):
        return 'user {}'.format(self.name)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    blog_text = db.Column(db.String(50), nullable=False)

    def __init__(self, name=None, blog=None):
        self.name = name
        self.blog_text = blog

    def __repr__(self):
        return 'user {}'.format(self.name)


db.create_all()
db.session.commit()

# some protected url
@app.route('/')
@login_required
def home():
    blogs = Blog.query.all()
    return render_template('layout.html', blogs=blogs)


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username:
            user = User(name=username, password=password)
            login_user(user)
            return redirect(url_for('home'))
        else:
            return abort(401)
    else:
        return render_template('login.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username:
            u = User(username, password)
            db.session.add(u)
            db.session.commit()
            login_user(u)
            return redirect(url_for('home'))
        else:
            return abort(401)
    else:
        return render_template('signup.html')


@app.route("/add_new_blog", methods=["GET", "POST"])
@login_required
def add_new_blog():
    if request.method == 'POST':
        owner = request.form['username']
        blog = request.form['blog']
        if owner:
            u = Blog(owner, blog)
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            return abort(401)
    else:
        return render_template('add_new_blog.html')

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)


if __name__ == "__main__":
    app.run()
