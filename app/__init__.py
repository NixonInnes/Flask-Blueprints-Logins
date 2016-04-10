from config import config
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    if not app.debug and not app.testing:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Add additional blueprints here...
    # example:
    # from .myblueprint import myblueprint as myblueprint_blueprint
    # app.register_blueprint(myblueprint_blueprint, url_prefix='/myblueprint')

    return app
