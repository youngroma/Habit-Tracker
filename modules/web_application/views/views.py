from flask import render_template, url_for, redirect, flash, Blueprint, request
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from modules.web_application.models.models import User, Habit, HabitPoint
from modules.web_application.forms.forms import RegistrationForm, LoginForm
import random
import matplotlib.pyplot as plt
import io
import base64
from flask import Response

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    return render_template('index.html')

@views.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@views.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@views.route('/dashboard')
@login_required
def dashboard():
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', habits=habits)

@views.route('/add_habit', methods=['GET', 'POST'])
@login_required
def add_habit():
    if request.method == 'POST':
        habit_name = request.form['habit_name']
        new_habit = Habit(name=habit_name, user_id=current_user.id)
        db.session.add(new_habit)
        db.session.commit()
        flash(f'New habit {habit_name} added!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_habit.html')




@views.route('/habit_graph/<int:habit_id>')
@login_required
def habit_graph(habit_id):
    habit = Habit.query.get_or_404(habit_id)

    points = habit.points.all()
    x_points = [point.x for point in points]
    y_points = [point.y for point in points]


    fig, ax = plt.subplots()
    ax.scatter(x_points, y_points, color='b')

    ax.set_title(f'Progress of Habit: {habit.name}')


    ax.set_xticks([])
    ax.set_yticks([])

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)

    img_base64 = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('habit_graph.html', habit_name=habit.name, img_base64=img_base64, habit_id=habit.id)

@views.route('/repeat_habit', methods=['POST'])
@login_required
def repeat_habit():
    habit_id = request.form.get('habit_id')
    habit = Habit.query.get_or_404(habit_id)

    habit.growth += 1

    new_x = random.uniform(0, 10)
    new_y = random.uniform(0, 10)

    new_point = HabitPoint(x=new_x, y=new_y, habit_id=habit.id)

    db.session.add(new_point)
    db.session.commit()

    flash(f'Habit "{habit.name}" marked as done! New point added at ({new_x:.2f}, {new_y:.2f})', 'success')

    return redirect(url_for('habit_graph', habit_id=habit_id))


@views.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
