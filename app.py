from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import CreateUser, LoginUser, FeedbackForm, UpdateFeedbackForm

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


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    if username == session["username"]:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        return redirect("/logout")
    else:
        flash("THAT AINT YOU THO")
        return redirect("/")


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):

    feedback = Feedback.query.get_or_404(feedback_id)
    form = UpdateFeedbackForm(obj=feedback)

    if feedback.username == session["username"]:
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data

            db.session.add(feedback)
            db.session.commit()
            return redirect(f"/users/{feedback.user.username}")
        else:
            return render_template("update-feedback-form.html", form=form,
                                   feedback=feedback)
    else:
        flash("BRO THIS FOR REAL AINT YOU")
        return redirect("/")


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):

    feedback = Feedback.query.get_or_404(feedback_id)
    feedback_username = session['username']
    if feedback.username == feedback_username:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback_username}")
    else:
        flash("IT AINT YOURS DONT TOUCH IT JEEZ")
        return redirect("/")


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
