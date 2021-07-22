from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from app import login

from hashlib import md5


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    """
    Inheriting UserMixin - part of the flask_login extention.
    Used to check if session belongs to an authentication user.
    It abstracts the tasks for checking if user is authenticated,
    if session is active, if user is anonymous, and to get user ID.

    Inheriting dB.Model - base class for all models of Flask-SQLAlchemy
    """
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username} email {self.email}>'

    def set_password(self, password):
        """
        Encrypting plaintext password using Werkzeug toolkit's function
        """
        self.password_hash = generate_password_hash(password)
        return
    
    def check_password(self, password):
        """
        Checking if password is valid using Werkzeug toolkit's function
        """
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?&s={size}'


    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())






class Post(db.Model):
    """
    Inheriting dB.Model - base class for all models of Flask-SQLAlchemy
    """
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id):
    """
    Flask-Login keeps track of the logged in user by storing its unique
    identifier in Flask's user session

    Returns a user object
    """
    return User.query.get(int(id))


