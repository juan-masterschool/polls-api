from flask import Blueprint, request, jsonify
from models import db, Poll, User, Option
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

polls_bp = Blueprint('polls', __name__, url_prefix='/api/polls')

@polls_bp.route('', methods=['GET'])
def get_polls():
    """Get all polls that the user can see"""
    polls = Poll.query.all()
    return jsonify([poll.to_dict() for poll in polls]), 200

@polls_bp.route('/<int:poll_id>', methods=['GET'])
def get_poll(poll_id):
    """Get a specific poll"""
    poll = Poll.query.get_or_404(poll_id)
    return jsonify(poll.to_dict()), 200

@polls_bp.route('', methods=['POST'])
@jwt_required()
def create_poll():
    """Create a new poll (requires authentication)"""
    data = request.get_json()
    
    if not data or not data.get('question'):
        return jsonify({'error': 'Question is required'}), 400
    
    if not data.get('options') or not isinstance(data.get('options'), list) or len(data.get('options')) < 2:
        return jsonify({'error': 'At least 2 options are required'}), 400
    
    # Validate and normalize options
    normalized_options = []
    seen_options = set()
    
    for option_text in data['options']:
        if not option_text or not isinstance(option_text, str):
            return jsonify({'error': 'All options must be non-empty strings'}), 400
        
        normalized = option_text.strip()
        if not normalized:
            return jsonify({'error': 'All options must be non-empty strings'}), 400
        
        # Check for duplicates (case-insensitive)
        normalized_lower = normalized.lower()
        if normalized_lower in seen_options:
            return jsonify({'error': 'Duplicate options are not allowed'}), 400
        
        seen_options.add(normalized_lower)
        normalized_options.append(normalized)
    
    user_id = int(get_jwt_identity())
    
    poll = Poll(
        question=data['question'],
        is_public=data.get('is_public', True),
        requires_admin=data.get('requires_admin', False),
        created_by=user_id
    )
    
    db.session.add(poll)
    db.session.flush()  # Get poll.id before committing
    
    # Create options
    for option_text in normalized_options:
        option = Option(poll_id=poll.id, text=option_text)
        db.session.add(option)
    
    db.session.commit()
    
    return jsonify(poll.to_dict()), 201

