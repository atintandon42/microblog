import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SOME_PARAMETER = "Yellow Submarine"
    SECRET_KEY = "No more sea surfing"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 7