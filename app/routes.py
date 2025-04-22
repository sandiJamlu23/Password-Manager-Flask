from flask import Blueprint, render_template, redirect, url_for, request
from .models import PasswordEntry
from . import db
from .crypto import encrypt_password, decrypt_password

main = Blueprint('main', __name__)

@main.route('/')
def index():
    entries = PasswordEntry.query.all()
    for entry in entries:
        entry.password = decrypt_password(entry.password)
    return render_template('index.html', entries=entries)

@main.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        account = request.form['account']
        username = request.form['username']
        password = encrypt_password(request.form['password'])

        new_entry = PasswordEntry(account=account, username=username, password=password)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('add.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
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
def delete(id):
    entry = PasswordEntry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('main.index'))
