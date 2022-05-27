from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user,login_required
from app import app

login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(email):
    return User(email=email)

#User schema
class User(UserMixin):
    def __init__(self, email):
        self.email = email
    def get_id(self):
        return self.email

def login(aEmail):
    user = User(email=aEmail)
    login_user(user)

def logout():
    print(f'Logging out {current_user.get_id()}')
    logout_user()