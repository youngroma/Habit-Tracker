from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from extensions import db
from modules.web_application.models.models import User
from modules.web_application.views.views import home, register, login, dashboard, add_habit, habit_graph, logout, views


def create_app():
    app = Flask(__name__, template_folder='modules/web_application/templates')
    app.config.from_object('config.config.Config')

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(views, url_prefix='/')
    app.add_url_rule('/', 'home', home)
    app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
    app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
    app.add_url_rule('/dashboard', 'dashboard', dashboard)
    app.add_url_rule('/add_habit', 'add_habit', add_habit, methods=['POST'])
    app.add_url_rule('/habit_graph/<int:habit_id>', 'habit_graph', habit_graph)
    app.add_url_rule('/logout', 'logout', logout)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
