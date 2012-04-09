from flask import Blueprint, render_template, flash, redirect, url_for
from flaskext.bcrypt import Bcrypt
from flaskext.login import LoginManager, login_user, login_required, logout_user

db = None

def create_users_blueprint(app, _db, login_redirect_view='main'):
    global db
    db = _db

    from .models import User
    from .forms import LoginForm, RegisterForm

    users_blueprint = Blueprint('users', __name__, template_folder='templates', static_folder='static')

    bcrypt = Bcrypt(app)

    login_manager = LoginManager()
    login_manager.setup_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def user_loader(user_id):
        return User.query.get(user_id)

    @users_blueprint.route('/login/', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or bcrypt.check_password_hash(user.password, form.password):
                flash("Invalid email or password", "error")
            else:
                login_user(user)
                flash("Login successful")
                return redirect(url_for('main'))
        return render_template('users/login.html', form=form)

    @users_blueprint.route('/logout/')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('main'))

    @users_blueprint.route('/register/', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            user = User(form.email.data, bcrypt.generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Login successful")
            return redirect(url_for(login_redirect_view))
        return render_template('users/register.html', form=form)

    return users_blueprint
