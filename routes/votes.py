from flask import Blueprint, request, jsonify
from models import db, Poll, Vote, User, Option
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError

votes_bp = Blueprint('votes', __name__, url_prefix='/api/votes')

def get_current_user():
    """Helper function to get current user if authenticated"""
    try:
        verify_jwt_in_request(optional=True)
        user_id_str = get_jwt_identity()
        if user_id_str:
            user_id = int(user_id_str)
            claims = get_jwt()
            return user_id, claims.get('is_admin', False)
        return None, False
    except (NoAuthorizationError, RuntimeError, ValueError):
        return None, False

@votes_bp.route('/poll/<int:poll_id>', methods=['POST'])
def vote(poll_id):
    """Vote on a poll with different access requirements"""
    poll = Poll.query.get_or_404(poll_id)
    data = request.get_json()
    
    if not data or not data.get('choice'):
        return jsonify({'error': 'Choice is required'}), 400
    
    user_id, is_admin = get_current_user()
    
    # Check if poll requires authentication
    if not poll.is_public and user_id is None:
        return jsonify({'error': 'Authentication required for this poll'}), 401
    
    # Check if poll requires admin
    if poll.requires_admin:
        if user_id is None:
            return jsonify({'error': 'Admin access required for this poll'}), 401
        if not is_admin:
            return jsonify({'error': 'Admin access required for this poll'}), 403
    
    # Validate that the poll has options
    if len(poll.options) == 0:
        return jsonify({'error': 'This poll has no options available'}), 400
    
    # Validate that the choice is one of the poll's options
    choice_text = data['choice'].strip()
    valid_options = [option.text for option in poll.options]
    
    if choice_text not in valid_options:
        return jsonify({
            'error': f'Invalid choice. Must be one of: {", ".join(valid_options)}'
        }), 400
    
    # Create vote
    vote = Vote(
        poll_id=poll_id,
        user_id=user_id,
        choice=choice_text
    )
    
    db.session.add(vote)
    db.session.commit()
    
    return jsonify(vote.to_dict()), 201

@votes_bp.route('/poll/<int:poll_id>', methods=['GET'])
def get_votes(poll_id):
    """Get all votes for a poll"""
    poll = Poll.query.get_or_404(poll_id)
    votes = Vote.query.filter_by(poll_id=poll_id).all()
    
    # Count votes by choice
    vote_counts = {}
    for vote in votes:
        vote_counts[vote.choice] = vote_counts.get(vote.choice, 0) + 1
    
    return jsonify({
        'poll': poll.to_dict(),
        'votes': [vote.to_dict() for vote in votes],
        'vote_counts': vote_counts
    }), 200

