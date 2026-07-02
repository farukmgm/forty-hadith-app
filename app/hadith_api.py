"""
Hadith API routes for retrieving and managing hadiths.
"""

from flask import Blueprint, jsonify, request
from app import db
from app.models import Hadith
from sqlalchemy import func

# Create hadith blueprint
hadith_bp = Blueprint('hadith_api', __name__, url_prefix='/api/hadiths')

@hadith_bp.route('', methods=['GET'])
def get_hadiths():
    """
    Get all hadiths with optional pagination and filtering.
    
    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Results per page (default: 10, max: 50)
    - search: Search term (searches in arabic_text and english_text)
    - hadith_number: Filter by specific hadith number
    
    Returns:
        JSON with hadiths list and pagination metadata
    """
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search_term = request.args.get('search', '', type=str)
        hadith_number = request.args.get('hadith_number', None, type=int)
        
        # Validate pagination parameters
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 50:
            per_page = 10
        
        # Build query
        query = Hadith.query
        
        # Apply filters
        if hadith_number:
            query = query.filter_by(hadith_number=hadith_number)
        
        if search_term:
            search_pattern = f'%{search_term}%'
            query = query.filter(
                db.or_(
                    Hadith.arabic_text.ilike(search_pattern),
                    Hadith.english_text.ilike(search_pattern),
                    Hadith.narrator.ilike(search_pattern)
                )
            )
        
        # Get total count before pagination
        total = query.count()
        
        # Apply pagination
        paginated = query.order_by(Hadith.hadith_number.asc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Format response
        hadiths = [
            {
                'id': h.id,
                'hadith_number': h.hadith_number,
                'arabic_text': h.arabic_text,
                'english_text': h.english_text,
                'narrator': h.narrator,
                'book_reference': h.book_reference,
                'source_url': h.source_url,
                'created_at': h.created_at.isoformat() if h.created_at else None
            }
            for h in paginated.items
        ]
        
        return jsonify({
            'status': 'success',
            'data': hadiths,
            'pagination': {
                'current_page': page,
                'per_page': per_page,
                'total_items': total,
                'total_pages': paginated.pages,
                'has_next': paginated.has_next,
                'has_prev': paginated.has_prev,
                'next_page': page + 1 if paginated.has_next else None,
                'prev_page': page - 1 if paginated.has_prev else None
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving hadiths: {str(e)}'
        }), 500

@hadith_bp.route('/<int:hadith_id>', methods=['GET'])
def get_hadith(hadith_id):
    """
    Get a single hadith by ID.
    
    Args:
        hadith_id: The ID of the hadith
    
    Returns:
        JSON with hadith details or 404 if not found
    """
    try:
        hadith = Hadith.query.get(hadith_id)
        
        if not hadith:
            return jsonify({
                'status': 'error',
                'message': f'Hadith with ID {hadith_id} not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': {
                'id': hadith.id,
                'hadith_number': hadith.hadith_number,
                'arabic_text': hadith.arabic_text,
                'english_text': hadith.english_text,
                'narrator': hadith.narrator,
                'book_reference': hadith.book_reference,
                'source_url': hadith.source_url,
                'created_at': hadith.created_at.isoformat() if hadith.created_at else None
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving hadith: {str(e)}'
        }), 500

@hadith_bp.route('/number/<int:hadith_number>', methods=['GET'])
def get_hadith_by_number(hadith_number):
    """
    Get a single hadith by hadith number (1-42).
    
    Args:
        hadith_number: The hadith number (1-42)
    
    Returns:
        JSON with hadith details or 404 if not found
    """
    try:
        hadith = Hadith.query.filter_by(hadith_number=hadith_number).first()
        
        if not hadith:
            return jsonify({
                'status': 'error',
                'message': f'Hadith number {hadith_number} not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': {
                'id': hadith.id,
                'hadith_number': hadith.hadith_number,
                'arabic_text': hadith.arabic_text,
                'english_text': hadith.english_text,
                'narrator': hadith.narrator,
                'book_reference': hadith.book_reference,
                'source_url': hadith.source_url,
                'created_at': hadith.created_at.isoformat() if hadith.created_at else None
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving hadith: {str(e)}'
        }), 500

@hadith_bp.route('/random', methods=['GET'])
def get_random_hadith():
    """
    Get a random hadith from the database.
    
    Returns:
        JSON with a random hadith
    """
    try:
        hadith = Hadith.query.order_by(func.random()).first()
        
        if not hadith:
            return jsonify({
                'status': 'error',
                'message': 'No hadiths found in database'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': {
                'id': hadith.id,
                'hadith_number': hadith.hadith_number,
                'arabic_text': hadith.arabic_text,
                'english_text': hadith.english_text,
                'narrator': hadith.narrator,
                'book_reference': hadith.book_reference,
                'source_url': hadith.source_url,
                'created_at': hadith.created_at.isoformat() if hadith.created_at else None
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving random hadith: {str(e)}'
        }), 500

@hadith_bp.route('/stats', methods=['GET'])
def get_hadith_stats():
    """
    Get statistics about hadiths in the database.
    
    Returns:
        JSON with hadith statistics
    """
    try:
        total_hadiths = Hadith.query.count()
        
        if total_hadiths == 0:
            return jsonify({
                'status': 'error',
                'message': 'No hadiths found in database'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': {
                'total_hadiths': total_hadiths,
                'min_hadith_number': db.session.query(func.min(Hadith.hadith_number)).scalar(),
                'max_hadith_number': db.session.query(func.max(Hadith.hadith_number)).scalar(),
                'narrators_count': db.session.query(func.count(func.distinct(Hadith.narrator))).scalar()
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving hadith statistics: {str(e)}'
        }), 500
