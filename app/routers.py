from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегистрировались!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()  # Откатить сессию при ошибке
            flash(f'Ошибка при регистрации: {str(e)}', 'danger')
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Неверно введены данные аккаунта', 'danger')
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/click')
@login_required
def click():
    current_user.clicks += 1
    db.session.commit()
    return redirect(url_for('index'))
