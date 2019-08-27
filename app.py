from flask import Flask, jsonify, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import CreateUser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def index():
    """redirects to register user page"""
    
    return redirect('/register')
    
@app.route('/register', methods=["GET", "POST"])
def register():
    """show form to create user"""
    
    form = CreateUser()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        new_user = User.register(username, password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect("/secret")
    else: 
        return render_template("register-user-form.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """login user to account"""
    
    form = LoginUser()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        
        if user:
            session["user_id"] = user.id
            return redirect("/secret")
        else: 
            form.username.errors = ["Bad name/password"]
    else:
        return render_template("login-user-form.html", form=form)