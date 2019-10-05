from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists


##########################DATABASE##################################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:***REMOVED_PASSWORD***@localhost/putbox'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db = SQLAlchemy(app)
Migrate(app, db)

if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'


##############################BLUEPRINTS################################
from project.core.views import core_blueprint
from project.users.views import users_blueprint
from project.admin.views import admin_blueprint
# from project.blog_posts.views import blogpost_blueprint
from project.error_pages.handler import error_page_blueprint

app.register_blueprint(core_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(users_blueprint)
# app.register_blueprint(blogpost_blueprint)
app.register_blueprint(error_page_blueprint)