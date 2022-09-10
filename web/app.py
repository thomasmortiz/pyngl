from flask import Flask
from flask_mongoengine import MongoEngine

db = MongoEngine()

def create_app(**config_overrides):
    app = Flask(__name__)

    # Load config
    app.config.from_pyfile('settings.py')

    # setup db
    db.init_app(app)

    # import blueprints
    from thermo.views import thermo_app

    # register blueprints
    app.register_blueprint(thermo_app)

    return app
