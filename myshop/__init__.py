from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY']='e8c037ddb45b5db20158c2c9927f03d4e81bdf81dc215aba6783f2c9d79cbeb3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

migrate=Migrate(app,db)
with app.app_context():
    if db.engine.url.drivername=="sqlite":
        migrate.init_app(app,db,render_as_batch=True)
    else:
        migrate.init_app(app,db)

login_manager=LoginManager(app)
login_manager.login_view='customer_login'
login_manager.login_message_category='info'
from myshop.admin import route
from myshop.products import route
from myshop.carts import carts
from myshop.customer import route
