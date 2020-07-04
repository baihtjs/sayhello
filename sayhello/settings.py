import os
import sys
from sayhello import app
#dev_db = 'sqlite:///' + os.path.join(os.path.dirname(app.root_path), 'data.db')
dev_db = 'sqlite:////' + os.path.join(os.path.dirname(app.root_path), 'data.db')
SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
DEBUG_TB_INTERCEPT_REDIRECTS = False
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)