import os 
from flask import Flask, session
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db

app = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()
app.secret_key = os.urandom(24)

from application.controllers import *

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5555, debug=True)
