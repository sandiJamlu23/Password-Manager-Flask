from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from .models import PasswordEntry, User
from . import db
from . import bcrypt
from . import login_manager
from .crypto import encrypt_password, decrypt_password
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
import pyotp
import time
import qrcode
import base64
from io import BytesIO

main = Blueprint('main', __name__)
settings_bp = Blueprint('settings', __name__, url_prefix='/setting')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# MAIN ROUTES
@main.route('/')
@login_required
def index():
    search_query = request.form.get('search', '') if request.method == 'POST' else request.args.get('search', '')

    if search_query:
        entries = PasswordEntry.query.filter(
            (PasswordEntry.account.ilike(f'%{search_query}%') |
            PasswordEntry.username.ilike(f'%{search_query}%'))
        ).all()
    else:
        entries = PasswordEntry.query.all()

    for entry in entries:
        entry.password = decrypt_password(entry.password)
    return render_template('index.html', entries=entries, search_query=search_query)

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
            # check if 2FA is enabled
            if user.is_2fa_enabled:
                session['2fa_user_id'] = user.id
                flash('2FA is enabled. Please enter your token.', 'info')
                return redirect(url_for('main.verify_2fa'))
            else:
                login_user(user)
                flash('Logged in successfully', 'success')
                return redirect(url_for('main.index'))
        else:
            flash('Login failed. Check your username and password', 'danger')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'success')
    return redirect(url_for('main.index'))

# Password Management Routes
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


# Settings Route (Placeholder)
# This route can be expanded later to include user settings, password policies, etc.
@main.route('/setting')
@login_required
def setting_dashboard():
    # user_id = session.get('user_id')
    user = current_user

    return render_template('settings/dashboard.html', user=user)

@main.route('/setting/security')
@login_required
def security_settings():
    user = current_user
    
    return render_template('settings/security.html', user=user)

@main.route('/2fa')
@login_required
def two_fa_settings():
    user = current_user
    
    return render_template('settings/2fa.html', user=user)

@main.route('/2fa/setup')
@login_required
def setup_2fa():
    user = current_user

    # Generate a secret key for 2FA setup
    secret = pyotp.random_base32()
    user.totp_secret = secret
    db.session.commit()

    # create time-based one-time password (TOTP) URI
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=user.username, issuer_name='PasswordManager')

    # generate qr code 
    img = qrcode.make(uri)
    buf = BytesIO()
    img.save(buf, format='PNG')
    qr_code = base64.b64encode(buf.getvalue()).decode('utf-8')

    # qrCode = generate_qr_code(secret, user.username)
    return render_template('settings/2fa_setup.html', uri=uri, user=user)

@main.route('/2fa/confirm-2fa', methods=['POST'])
@login_required
def confirm_2fa():
    # user_id = session.get('user_id')
    user = current_user
    token = request.form.get('token')

    totp = pyotp.TOTP(user.totp_secret)

    # verify the token entered by user vs. totp.now
    if totp.verify() == token:
        user.is_2fa_enabled = True
        db.session.commit()
        flash('2FA has been enabled successfully.', 'success')
        return redirect(url_for('main.index'))
    return render_template('settings/2fa.html', user=user, error='Invalid token. Please try again.')

@main.route('/setting/2fa/disable', methods=['POST'])
@login_required
def disable_2fa():
    user = current_user
    
    # Ask for current password for security
    current_password = request.form.get('current_password')
    
    if not bcrypt.check_password_hash(user.password, current_password):
        flash('Invalid password. Cannot disable 2FA.', 'danger')
        return redirect(url_for('main.two_fa_settings'))
    
    # Disable 2FA
    user.is_2fa_enabled = False
    user.totp_secret = None  # Clear the secret
    db.session.commit()
    
    flash('2FA has been disabled.', 'success')
    return redirect(url_for('main.security_settings'))

# Add this route to handle 2FA verification during login
@main.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    # This should only be accessible if user is partially logged in
    if not session.get('2fa_user_id'):
        flash('Access denied.', 'danger')
        return redirect(url_for('main.login'))
    if request.method == 'POST':
        token = request.form.get('token')
        user_id = session.get('2fa_user_id')
        user = User.query.get(user_id)
        
        totp = pyotp.TOTP(user.totp_secret)
        
        if totp.verify(token, valid_window=1):
            # Complete the login
            login_user(user)
            session.pop('2fa_user_id', None)
            flash('Successfully logged in with 2FA!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid 2FA code. Please try again.', 'danger')
    
    return render_template('verify_2fa.html')