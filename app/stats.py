"""
Statistics and Streak Tracking API endpoints
Handles user statistics, streaks, and achievement tracking
"""

from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models import UserStats, UserProgress, DailyReview, User
from datetime import datetime, date, timedelta
from sqlalchemy import func

stats_bp = Blueprint('stats', __name__, url_prefix='/api/stats')

# ============================================================================
# STATISTICS CALCULATION FUNCTIONS
# ============================================================================

def calculate_user_statistics(user_id):
    """
    Calculate comprehensive statistics for a user.
    Updates the UserStats record in the database.
    
    Returns: UserStats object with updated values
    """
    # Count total memorized hadiths
    total_memorized = UserProgress.query.filter_by(
        user_id=user_id,
        is_memorized=True
    ).count()
    
    # Count total reviewed hadiths
    total_reviewed = UserProgress.query.filter_by(
        user_id=user_id
    ).filter(UserProgress.reviewed_count > 0).count()
    
    # Calculate current streak
    current_streak = calculate_current_streak(user_id)
    
    # Get longest streak
    longest_streak = get_longest_streak(user_id)
    
    # Get last review date
    last_progress = UserProgress.query.filter_by(user_id=user_id).order_by(
        UserProgress.last_reviewed_at.desc()
    ).first()
    last_review_date = last_progress.last_reviewed_at.date() if last_progress and last_progress.last_reviewed_at else None
    
    # Get or create UserStats record
    user_stats = UserStats.query.filter_by(user_id=user_id).first()
    if not user_stats:
        user_stats = UserStats(user_id=user_id)
        db.session.add(user_stats)
    
    # Update statistics
    user_stats.total_memorized = total_memorized
    user_stats.total_reviewed = total_reviewed
    user_stats.current_streak = current_streak
    user_stats.longest_streak = longest_streak
    user_stats.last_review_date = last_review_date
    user_stats.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return user_stats


def calculate_current_streak(user_id):
    """
    Calculate the current streak (consecutive days with at least 1 review).
    
    Streak logic:
    - Gets the most recent daily reviews
    - Counts backwards from today
    - Stops when a day is skipped
    
    Returns: Integer representing current streak length
    """
    today = date.today()
    streak = 0
    current_date = today
    
    while True:
        # Check if user reviewed at least one hadith on this date
        daily_review = DailyReview.query.filter_by(
            user_id=user_id,
            review_date=current_date
        ).first()
        
        if daily_review:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return streak


def get_longest_streak(user_id):
    """
    Calculate the longest streak ever achieved by the user.
    
    Returns: Integer representing longest streak length
    """
    # Get all daily reviews sorted by date
    daily_reviews = DailyReview.query.filter_by(user_id=user_id).order_by(
        DailyReview.review_date.asc()
    ).all()
    
    if not daily_reviews:
        return 0
    
    max_streak = 0
    current_streak = 1
    
    for i in range(1, len(daily_reviews)):
        prev_date = daily_reviews[i - 1].review_date
        curr_date = daily_reviews[i].review_date
        
        # Check if consecutive days
        if (curr_date - prev_date).days == 1:
            current_streak += 1
        else:
            max_streak = max(max_streak, current_streak)
            current_streak = 1
    
    max_streak = max(max_streak, current_streak)
    
    return max_streak


def log_daily_review(user_id, hadith_id):
    """
    Log a hadith review for today.
    Creates or updates DailyReview record.
    
    Args:
        user_id: User ID
        hadith_id: Hadith ID being reviewed
    """
    today = date.today()
    
    # Get or create daily review record
    daily_review = DailyReview.query.filter_by(
        user_id=user_id,
        review_date=today
    ).first()
    
    if not daily_review:
        daily_review = DailyReview(
            user_id=user_id,
            review_date=today,
            hadith_ids_reviewed=str(hadith_id)
        )
        db.session.add(daily_review)
    else:
        # Append hadith_id to existing list if not already present
        ids = daily_review.hadith_ids_reviewed.split(',') if daily_review.hadith_ids_reviewed else []
        hadith_id_str = str(hadith_id)
        if hadith_id_str not in ids:
            ids.append(hadith_id_str)
            daily_review.hadith_ids_reviewed = ','.join(ids)
    
    db.session.commit()


def reset_daily_reviews():
    """
    Reset is_reviewed_today flag for all users at midnight.
    This should be called by a scheduled task (e.g., APScheduler).
    
    Note: In production, this should be handled by a background job.
    For now, it can be called manually or via a cron job.
    """
    # Reset is_reviewed_today for all records
    UserProgress.query.update({'is_reviewed_today': False})
    db.session.commit()


# ============================================================================
# STATISTICS ENDPOINTS
# ============================================================================

@stats_bp.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_user_stats(user_id):
    """
    Get statistics for a specific user.
    
    URL Parameters:
    - user_id: <int> - User ID
    
    Response:
    {
        "status": "success",
        "data": {
            "user_id": <int>,
            "username": "<string>",
            "total_memorized": <int>,
            "total_reviewed": <int>,
            "current_streak": <int>,
            "longest_streak": <int>,
            "last_review_date": "YYYY-MM-DD",
            "updated_at": "ISO timestamp",
            "achievements": {
                "memorized_all_42": <bool>,
                "reviewed_all_42_today": <bool>,
                "seven_day_streak": <bool>,
                "thirty_day_streak": <bool>
            }
        }
    }
    """
    try:
        # Verify user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'User with ID {user_id} not found'
            }), 404
        
        # Users can only view their own stats (or admins can view all)
        if current_user.id != user_id:
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized: You can only view your own statistics'
            }), 403
        
        # Calculate fresh statistics
        user_stats = calculate_user_statistics(user_id)
        
        # Check achievements
        achievements = {
            'memorized_all_42': user_stats.total_memorized == 42,
            'reviewed_all_42_today': user_stats.total_reviewed == 42,
            'seven_day_streak': user_stats.current_streak >= 7,
            'thirty_day_streak': user_stats.current_streak >= 30
        }
        
        return jsonify({
            'status': 'success',
            'data': {
                'user_id': user.id,
                'username': user.username,
                'total_memorized': user_stats.total_memorized,
                'total_reviewed': user_stats.total_reviewed,
                'current_streak': user_stats.current_streak,
                'longest_streak': user_stats.longest_streak,
                'last_review_date': user_stats.last_review_date.isoformat() if user_stats.last_review_date else None,
                'updated_at': user_stats.updated_at.isoformat(),
                'achievements': achievements
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error retrieving user statistics: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500


@stats_bp.route('/user/<int:user_id>/breakdown', methods=['GET'])
@login_required
def get_user_stats_breakdown(user_id):
    """
    Get detailed breakdown of user statistics.
    
    URL Parameters:
    - user_id: <int> - User ID
    
    Response:
    {
        "status": "success",
        "data": {
            "overview": { ... },
            "memorization_breakdown": {
                "memorized": <int>,
                "not_memorized": <int>,
                "total": <int>,
                "percentage": <float>
            },
            "review_breakdown": {
                "reviewed_today": <int>,
                "not_reviewed_today": <int>,
                "total": <int>
            },
            "reflection_stats": {
                "with_reflection": <int>,
                "without_reflection": <int>,
                "total": <int>
            },
            "streak_info": {
                "current_streak": <int>,
                "longest_streak": <int>,
                "average_reviews_per_day": <float>
            }
        }
    }
    """
    try:
        # Verify user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'User with ID {user_id} not found'
            }), 404
        
        # Users can only view their own stats
        if current_user.id != user_id:
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized: You can only view your own statistics'
            }), 403
        
        # Get overview stats
        user_stats = calculate_user_statistics(user_id)
        
        # Get memorization breakdown
        memorized = UserProgress.query.filter_by(user_id=user_id, is_memorized=True).count()
        not_memorized = UserProgress.query.filter_by(user_id=user_id, is_memorized=False).count()
        total = UserProgress.query.filter_by(user_id=user_id).count()
        memorization_percentage = (memorized / total * 100) if total > 0 else 0
        
        # Get review breakdown
        reviewed_today = UserProgress.query.filter_by(user_id=user_id, is_reviewed_today=True).count()
        not_reviewed_today = total - reviewed_today
        
        # Get reflection stats
        with_reflection = db.session.query(func.count(UserProgress.id)).filter(
            UserProgress.user_id == user_id,
            UserProgress.reflection_text.isnot(None),
            UserProgress.reflection_text != ''
        ).scalar()
        without_reflection = total - with_reflection
        
        # Calculate average reviews per day
        all_daily_reviews = DailyReview.query.filter_by(user_id=user_id).count()
        days_active = (datetime.utcnow().date() - user.created_at.date()).days + 1
        average_reviews_per_day = (all_daily_reviews / days_active) if days_active > 0 else 0
        
        return jsonify({
            'status': 'success',
            'data': {
                'overview': {
                    'total_memorized': user_stats.total_memorized,
                    'total_reviewed': user_stats.total_reviewed,
                    'current_streak': user_stats.current_streak,
                    'longest_streak': user_stats.longest_streak
                },
                'memorization_breakdown': {
                    'memorized': memorized,
                    'not_memorized': not_memorized,
                    'total': total,
                    'percentage': round(memorization_percentage, 2)
                },
                'review_breakdown': {
                    'reviewed_today': reviewed_today,
                    'not_reviewed_today': not_reviewed_today,
                    'total': total
                },
                'reflection_stats': {
                    'with_reflection': with_reflection,
                    'without_reflection': without_reflection,
                    'total': total
                },
                'streak_info': {
                    'current_streak': user_stats.current_streak,
                    'longest_streak': user_stats.longest_streak,
                    'average_reviews_per_day': round(average_reviews_per_day, 2)
                }
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error retrieving user statistics breakdown: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500


@stats_bp.route('/leaderboard', methods=['GET'])
@login_required
def get_leaderboard():
    """
    Get leaderboard of top users by various metrics.
    
    Query Parameters:
    - metric: 'memorized' (default), 'streak', 'reviewed'
    - limit: Number of users to return (default: 10, max: 100)
    
    Response:
    {
        "status": "success",
        "metric": "<string>",
        "limit": <int>,
        "data": [
            {
                "rank": <int>,
                "user_id": <int>,
                "username": "<string>",
                "value": <int>
            },
            ...
        ]
    }
    """
    try:
        metric = request.args.get('metric', 'memorized')
        limit = min(int(request.args.get('limit', 10)), 100)
        
        if metric == 'memorized':
            # Top users by total memorized hadiths
            results = db.session.query(
                User.id,
                User.username,
                func.count(UserProgress.id).label('value')
            ).join(UserProgress, User.id == UserProgress.user_id).filter(
                UserProgress.is_memorized == True
            ).group_by(User.id, User.username).order_by(
                func.count(UserProgress.id).desc()
            ).limit(limit).all()
        
        elif metric == 'streak':
            # Top users by current streak
            results = db.session.query(
                User.id,
                User.username,
                UserStats.current_streak.label('value')
            ).join(UserStats, User.id == UserStats.user_id).order_by(
                UserStats.current_streak.desc()
            ).limit(limit).all()
        
        elif metric == 'reviewed':
            # Top users by total reviews
            results = db.session.query(
                User.id,
                User.username,
                func.count(UserProgress.id).label('value')
            ).join(UserProgress, User.id == UserProgress.user_id).filter(
                UserProgress.reviewed_count > 0
            ).group_by(User.id, User.username).order_by(
                func.count(UserProgress.id).desc()
            ).limit(limit).all()
        
        else:
            return jsonify({
                'status': 'error',
                'message': f'Invalid metric: {metric}'
            }), 400
        
        # Format results
        leaderboard = []
        for rank, (user_id, username, value) in enumerate(results, 1):
            leaderboard.append({
                'rank': rank,
                'user_id': user_id,
                'username': username,
                'value': value
            })
        
        return jsonify({
            'status': 'success',
            'metric': metric,
            'limit': limit,
            'data': leaderboard
        }), 200
        
    except ValueError:
        return jsonify({
            'status': 'error',
            'message': 'Invalid query parameters'
        }), 400
    except Exception as e:
        current_app.logger.error(f'Error retrieving leaderboard: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500


@stats_bp.route('/user/<int:user_id>/activity', methods=['GET'])
@login_required
def get_user_activity(user_id):
    """
    Get user's activity history (daily reviews).
    
    URL Parameters:
    - user_id: <int> - User ID
    
    Query Parameters:
    - days: Number of past days to retrieve (default: 30)
    
    Response:
    {
        "status": "success",
        "user_id": <int>,
        "days": <int>,
        "data": [
            {
                "date": "YYYY-MM-DD",
                "hadiths_reviewed": <int>,
                "review_count": <int>
            },
            ...
        ]
    }
    """
    try:
        # Verify user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'User with ID {user_id} not found'
            }), 404
        
        # Users can only view their own activity
        if current_user.id != user_id:
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized: You can only view your own activity'
            }), 403
        
        days = int(request.args.get('days', 30))
        start_date = date.today() - timedelta(days=days)
        
        # Get daily reviews for the period
        daily_reviews = DailyReview.query.filter(
            DailyReview.user_id == user_id,
            DailyReview.review_date >= start_date
        ).order_by(DailyReview.review_date.desc()).all()
        
        # Format response
        activity_data = []
        for review in daily_reviews:
            hadith_ids = review.hadith_ids_reviewed.split(',') if review.hadith_ids_reviewed else []
            activity_data.append({
                'date': review.review_date.isoformat(),
                'hadiths_reviewed': len(hadith_ids),
                'review_count': len(hadith_ids)
            })
        
        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'days': days,
            'data': activity_data
        }), 200
        
    except ValueError:
        return jsonify({
            'status': 'error',
            'message': 'Invalid query parameters'
        }), 400
    except Exception as e:
        current_app.logger.error(f'Error retrieving user activity: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500
