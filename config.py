WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]


import os
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLalchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False # explictly set to suppress warnings

# Flask-WhooshAlchemy search db
WHOOSH_BASE = os.path.join(basedir, 'search.db')

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# admin list
ADMINS = ['you@example.com']
# command to run the above debugging email server locally
# python3 -m smtpd -n -c DebuggingServer localhost:25


#pagination
POSTS_PER_PAGE = 10
