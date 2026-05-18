from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Hadith, UserProgress, UserStats

# Create blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
hadith_bp = Blueprint('hadith', __name__)
progress_bp = Blueprint('progress', __name__)
stats_bp = Blueprint('stats', __name__)

# Main Routes
@main_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user_stats = UserStats.query.filter_by(user_id=current_user.id).first()
    return render_template('dashboard.html', stats=user_stats)

# Authentication Routes (To be implemented)
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    # TODO: Implement registration
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    # TODO: Implement login
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    # TODO: Implement logout
    pass

# Hadith Routes (To be implemented)
@hadith_bp.route('/')
def list_hadiths():
    """List all hadiths"""
    hadiths = Hadith.query.order_by(Hadith.hadith_number).all()
    return render_template('hadiths.html', hadiths=hadiths)

@hadith_bp.route('/<int:hadith_id>')
def view_hadith(hadith_id):
    """View single hadith"""
    hadith = Hadith.query.get_or_404(hadith_id)
    user_progress = None
    if current_user.is_authenticated:
        user_progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            hadith_id=hadith_id
        ).first()
    return render_template('hadith.html', hadith=hadith, progress=user_progress)

# Progress Routes (To be implemented)
@progress_bp.route('/mark-reviewed', methods=['POST'])
@login_required
def mark_reviewed():
    """Mark hadith as reviewed today"""
    # TODO: Implement mark reviewed
    return jsonify({'success': True})

@progress_bp.route('/mark-memorized', methods=['POST'])
@login_required
def mark_memorized():
    """Mark hadith as memorized"""
    # TODO: Implement mark memorized
    return jsonify({'success': True})

@progress_bp.route('/save-reflection', methods=['POST'])
@login_required
def save_reflection():
    """Save reflection for hadith"""
    # TODO: Implement save reflection
    return jsonify({'success': True})

@progress_bp.route('/user/<int:user_id>')
@login_required
def user_progress(user_id):
    """Get user's progress"""
    # TODO: Implement get progress
    pass

# Statistics Routes (To be implemented)
@stats_bp.route('/user/<int:user_id>')
@login_required
def user_stats(user_id):
    """Get user statistics"""
    # TODO: Implement get stats
    pass

@stats_bp.route('/page')
@login_required
def stats_page():
    """Statistics page"""
    user_stats = UserStats.query.filter_by(user_id=current_user.id).first()
    return render_template('stats.html', stats=user_stats)
