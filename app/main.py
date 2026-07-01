"""
Main application routes for dashboard and main pages.
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

# Create main blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard route"""
    return render_template('dashboard.html', user=current_user)

@main_bp.route('/hadiths')
@login_required
def hadiths():
    """Hadiths list page route"""
    return render_template('hadiths.html')

@main_bp.route('/progress')
@login_required
def progress():
    """User progress page route"""
    return render_template('progress.html', user=current_user)

@main_bp.route('/stats')
@login_required
def stats():
    """User statistics page route"""
    return render_template('stats.html', user=current_user)
