from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import CreateUser, LoginUser, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)


@app.route("/")
def index():
    """redirects to register user page"""

    return redirect('/register')


@app.route("/register", methods=["GET", "POST"])
def register():
    """show form to create user"""

    form = CreateUser()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email,
                                 first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        session["username"] = username
        return redirect(f"/users/{new_user.username}")
    else:
        return render_template("register-user-form.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """login user to account"""

    form = LoginUser()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Bad name/password"]
    else:
        return render_template("login-user-form.html", form=form)


@app.route("/users/<username>")
def show_user_page(username):

    if username == session["username"]:
        user = User.query.get_or_404(username)
        feedbacks = Feedback.query.filter_by(username=username).all()
        return render_template("user_page.html", user=user,
                               feedbacks=feedbacks)
    else:
        flash("That ain't you")
        return redirect("/login")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):

    form = FeedbackForm()

    if form.validate_on_submit():
        if username == session["username"]:

            new_feedback = Feedback()
            new_feedback.title = form.title.data
            new_feedback.content = form.content.data
            new_feedback.username = username

            db.session.add(new_feedback)
            db.session.commit()
            return redirect(f"/users/{username}")
        else:
            flash("That ain't you")
            return redirect("/login")
    else:
        return render_template("add-feedback-form.html", form=form)


@app.route('/secret')
def show_secret():
    """Make sure user is logged in then show secret page"""
    if "username" not in session:
        flash("You gotta log in bro")
        return redirect("/")
    return "YOU MADE IT"


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
