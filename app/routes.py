from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import PasswordEntry, User
from . import db
from . import bcrypt
from . import login_manager
from .crypto import encrypt_password, decrypt_password
from flask_login import UserMixin, login_user, logout_user, login_required, current_user

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def index():
    entries = PasswordEntry.query.all()
    for entry in entries:
        entry.password = decrypt_password(entry.password)
    return render_template('index.html', entries=entries)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('main.register'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration Success. Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully❤️', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login failed. Check your username and password, Dumbass', 'danger')
    return render_template('login.html')
    

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'success')
    return redirect(url_for('main.index'))

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        site = request.form['site']
        username = request.form['username']
        password = encrypt_password(request.form['password'])

        new_entry = PasswordEntry(account=site, username=username, password=password)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('add.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    entry = PasswordEntry.query.get_or_404(id)

    if request.method == 'POST':
        entry.account = request.form['account']
        entry.username = request.form['username']
        entry.password = encrypt_password(request.form['password'])
        db.session.commit()
        return redirect(url_for('main.index'))

    entry.password = decrypt_password(entry.password)
    return render_template('edit.html', entry=entry)


@main.route('/delete/<int:id>')
@login_required
def delete(id):
    entry = PasswordEntry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/security')
@login_required
def security():
    entries = PasswordEntry.query.all()
    reused = {}
    
    if entries:  # Only process if there are entries
        # Decrypt all passwords and count their occurrences
        from app.crypto import decrypt_password
        password_counts = {}
        for entry in entries:
            pwd = decrypt_password(entry.password)
            password_counts[pwd] = password_counts.get(pwd, 0) + 1
        
        reused = {p: c for p, c in password_counts.items() if c > 1}
    
    return render_template('security.html', entries=entries, reused=reused)
