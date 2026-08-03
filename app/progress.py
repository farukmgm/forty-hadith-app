"""
Progress tracking API endpoints
Handles user progress tracking for hadiths (reviews, memorization, reflections)
"""

from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models import UserProgress, Hadith, User, UserStats
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError

progress_bp = Blueprint('progress', __name__, url_prefix='/api/progress')

# ============================================================================
# PROGRESS TRACKING ENDPOINTS
# ============================================================================

@progress_bp.route('/mark-reviewed', methods=['POST'])
@login_required
def mark_reviewed():
    """
    Mark a hadith as reviewed today for the current user.
    
    Request body (JSON):
    {
        "hadith_id": <int>
    }
    
    Response:
    {
        "status": "success",
        "message": "Hadith marked as reviewed",
        "data": {
            "user_id": <int>,
            "hadith_id": <int>,
            "is_reviewed_today": true,
            "last_reviewed_at": "ISO timestamp",
            "reviewed_count": <int>
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'hadith_id' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: hadith_id'
            }), 400
        
        hadith_id = data.get('hadith_id')
        user_id = current_user.id
        
        # Verify hadith exists
        hadith = Hadith.query.get(hadith_id)
        if not hadith:
            return jsonify({
                'status': 'error',
                'message': f'Hadith with ID {hadith_id} not found'
            }), 404
        
        # Get or create progress record
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            hadith_id=hadith_id
        ).first()
        
        if not progress:
            progress = UserProgress(
                user_id=user_id,
                hadith_id=hadith_id
            )
            db.session.add(progress)
        
        # Update progress
        progress.is_reviewed_today = True
        progress.last_reviewed_at = datetime.utcnow()
        progress.reviewed_count = (progress.reviewed_count or 0) + 1
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Hadith marked as reviewed',
            'data': {
                'user_id': progress.user_id,
                'hadith_id': progress.hadith_id,
                'is_reviewed_today': progress.is_reviewed_today,
                'last_reviewed_at': progress.last_reviewed_at.isoformat() if progress.last_reviewed_at else None,
                'reviewed_count': progress.reviewed_count
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error marking hadith as reviewed: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500


@progress_bp.route('/mark-memorized', methods=['POST'])
@login_required
def mark_memorized():
    """
    Mark a hadith as memorized for the current user.
    
    Request body (JSON):
    {
        "hadith_id": <int>,
        "is_memorized": <bool>  (true to memorize, false to un-memorize)
    }
    
    Response:
    {
        "status": "success",
        "message": "Hadith marked as memorized",
        "data": {
            "user_id": <int>,
            "hadith_id": <int>,
            "is_memorized": true,
            "updated_at": "ISO timestamp"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'hadith_id' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: hadith_id'
            }), 400
        
        hadith_id = data.get('hadith_id')
        is_memorized = data.get('is_memorized', True)
        user_id = current_user.id
        
        # Verify hadith exists
        hadith = Hadith.query.get(hadith_id)
        if not hadith:
            return jsonify({
                'status': 'error',
                'message': f'Hadith with ID {hadith_id} not found'
            }), 404
        
        # Get or create progress record
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            hadith_id=hadith_id
        ).first()
        
        if not progress:
            progress = UserProgress(
                user_id=user_id,
                hadith_id=hadith_id
            )
            db.session.add(progress)
        
        # Update memorization status
        progress.is_memorized = is_memorized
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Hadith memorization status updated',
            'data': {
                'user_id': progress.user_id,
                'hadith_id': progress.hadith_id,
                'is_memorized': progress.is_memorized,
                'updated_at': progress.updated_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error marking hadith as memorized: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500


@progress_bp.route('/save-reflection', methods=['POST'])
@login_required
def save_reflection():
    """
    Save or update reflection text for a hadith.
    
    Request body (JSON):
    {
        "hadith_id": <int>,
        "reflection_text": "<string>"
    }
    
    Response:
    {
        "status": "success",
        "message": "Reflection saved",
        "data": {
            "user_id": <int>,
            "hadith_id": <int>,
            "reflection_text": "<string>",
            "updated_at": "ISO timestamp"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'hadith_id' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: hadith_id'
            }), 400
        
        hadith_id = data.get('hadith_id')
        reflection_text = data.get('reflection_text', '')
        user_id = current_user.id
        
        # Verify hadith exists
        hadith = Hadith.query.get(hadith_id)
        if not hadith:
            return jsonify({
                'status': 'error',
                'message': f'Hadith with ID {hadith_id} not found'
            }), 404
        
        # Get or create progress record
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            hadith_id=hadith_id
        ).first()
        
        if not progress:
            progress = UserProgress(
                user_id=user_id,
                hadith_id=hadith_id
            )
            db.session.add(progress)
        
        # Save reflection
        progress.reflection_text = reflection_text
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Reflection saved',
            'data': {
                'user_id': progress.user_id,
                'hadith_id': progress.hadith_id,
                'reflection_text': progress.reflection_text,
                'updated_at': progress.updated_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error saving reflection: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500


@progress_bp.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_user_progress(user_id):
    """
    Get all progress records for a specific user.
    
    URL Parameters:
    - user_id: <int> - User ID
    
    Query Parameters:
    - hadith_id (optional): Filter by specific hadith
    - memorized_only (optional): Set to 'true' to show only memorized hadiths
    - reviewed_only (optional): Set to 'true' to show only reviewed hadiths
    
    Response:
    {
        "status": "success",
        "user_id": <int>,
        "total_records": <int>,
        "statistics": {
            "total_memorized": <int>,
            "total_reviewed": <int>,
            "current_streak": <int>
        },
        "data": [
            {
                "id": <int>,
                "hadith_id": <int>,
                "hadith_number": <int>,
                "is_memorized": <bool>,
                "is_reviewed_today": <bool>,
                "last_reviewed_at": "ISO timestamp",
                "reviewed_count": <int>,
                "reflection_text": "<string>",
                "created_at": "ISO timestamp",
                "updated_at": "ISO timestamp"
            },
            ...
        ]
    }
    """
    try:
        # Verify user exists and user has permission
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'User with ID {user_id} not found'
            }), 404
        
        # Users can only view their own progress (or admins can view all)
        if current_user.id != user_id:
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized: You can only view your own progress'
            }), 403
        
        # Build query
        query = UserProgress.query.filter_by(user_id=user_id)
        
        # Apply filters
        hadith_id_filter = request.args.get('hadith_id', type=int)
        if hadith_id_filter:
            query = query.filter_by(hadith_id=hadith_id_filter)
        
        memorized_only = request.args.get('memorized_only', 'false').lower() == 'true'
        if memorized_only:
            query = query.filter_by(is_memorized=True)
        
        reviewed_only = request.args.get('reviewed_only', 'false').lower() == 'true'
        if reviewed_only:
            query = query.filter_by(is_reviewed_today=True)
        
        # Get results
        progress_records = query.all()
        
        # Calculate statistics
        total_memorized = UserProgress.query.filter_by(
            user_id=user_id,
            is_memorized=True
        ).count()
        
        total_reviewed = UserProgress.query.filter_by(
            user_id=user_id,
            is_reviewed_today=True
        ).count()
        
        # Get or create user stats
        user_stats = UserStats.query.filter_by(user_id=user_id).first()
        current_streak = user_stats.current_streak if user_stats else 0
        
        # Format response
        progress_data = []
        for progress in progress_records:
            progress_data.append({
                'id': progress.id,
                'hadith_id': progress.hadith_id,
                'hadith_number': progress.hadith.hadith_number,
                'is_memorized': progress.is_memorized,
                'is_reviewed_today': progress.is_reviewed_today,
                'last_reviewed_at': progress.last_reviewed_at.isoformat() if progress.last_reviewed_at else None,
                'reviewed_count': progress.reviewed_count,
                'reflection_text': progress.reflection_text,
                'created_at': progress.created_at.isoformat(),
                'updated_at': progress.updated_at.isoformat()
            })
        
        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'total_records': len(progress_records),
            'statistics': {
                'total_memorized': total_memorized,
                'total_reviewed': total_reviewed,
                'current_streak': current_streak
            },
            'data': progress_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error retrieving user progress: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500


@progress_bp.route('/hadith/<int:hadith_id>/users', methods=['GET'])
@login_required
def get_hadith_users_progress(hadith_id):
    """
    Get progress stats for all users on a specific hadith (admin only).
    
    URL Parameters:
    - hadith_id: <int> - Hadith ID
    
    Response:
    {
        "status": "success",
        "hadith_id": <int>,
        "hadith_number": <int>,
        "total_users": <int>,
        "users_memorized": <int>,
        "users_reviewed": <int>,
        "data": [
            {
                "user_id": <int>,
                "username": "<string>",
                "is_memorized": <bool>,
                "is_reviewed_today": <bool>,
                "last_reviewed_at": "ISO timestamp"
            },
            ...
        ]
    }
    """
    try:
        # Verify hadith exists
        hadith = Hadith.query.get(hadith_id)
        if not hadith:
            return jsonify({
                'status': 'error',
                'message': f'Hadith with ID {hadith_id} not found'
            }), 404
        
        # Get all progress records for this hadith
        progress_records = UserProgress.query.filter_by(hadith_id=hadith_id).all()
        
        # Calculate statistics
        total_users = len(progress_records)
        users_memorized = sum(1 for p in progress_records if p.is_memorized)
        users_reviewed = sum(1 for p in progress_records if p.is_reviewed_today)
        
        # Format response
        users_data = []
        for progress in progress_records:
            users_data.append({
                'user_id': progress.user.id,
                'username': progress.user.username,
                'is_memorized': progress.is_memorized,
                'is_reviewed_today': progress.is_reviewed_today,
                'last_reviewed_at': progress.last_reviewed_at.isoformat() if progress.last_reviewed_at else None
            })
        
        return jsonify({
            'status': 'success',
            'hadith_id': hadith_id,
            'hadith_number': hadith.hadith_number,
            'total_users': total_users,
            'users_memorized': users_memorized,
            'users_reviewed': users_reviewed,
            'data': users_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error retrieving hadith progress: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500
