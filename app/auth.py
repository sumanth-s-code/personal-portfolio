"""
Authentication module for the Personal Portfolio app.

Provides routes for admin login and logout.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Admin login route.

    GET: Render the login form.
    POST: Process login credentials.
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if username == current_app.config['ADMIN_USERNAME'] and password == current_app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            flash('Logged in successfully.', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('admin_login.html')


@bp.route('/logout')
def logout():
    """
    Admin logout route.
    """
    session.pop('admin_logged_in', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login'))

