from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    
class User(db.Model):
    """sets up a user"""
    
    __tablename__ = "users"
    
    username = db.Column(db.String(20),
                         primary_key=True,
                         nullable=False)
    password = db.Column(db.Text,
                         nullable=False)
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String(30),
                     nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    
    @classmethod
    def register(cls, username, pwd):
        """register user with hashed password and return user"""
        
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        
        return cls(username=username, password=hashed_utf8)
    
    @classmethod
    def authenticate(cls, username, pwd):
        """authenticate a user"""
        
        u = User.query.filter_by(username=username).first()
        
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else: 
            return False