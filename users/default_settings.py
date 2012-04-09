import os

from .users import app

SECRET_KEY = "MY SECRET KEY"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.instance_path, 'campaign.sqlite')
