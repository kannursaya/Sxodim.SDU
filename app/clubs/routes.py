from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Club, ClubMembership, User

bp = Blueprint('clubs', __name__)

@bp.route('/', methods=['GET'])
def get_clubs():
    clubs = Club.query.all()
    return jsonify([{
        'id': club.id,
        'name': club.name,
        'description': club.description,
        'logo_url': club.logo_url,
        'member_count': club.members.count()
    } for club in clubs]), 200

@bp.route('/<int:club_id>', methods=['GET'])
def get_club(club_id):
    club = Club.query.get_or_404(club_id)
    return jsonify({
        'id': club.id,
        'name': club.name,
        'description': club.description,
        'logo_url': club.logo_url,
        'member_count': club.members.count()
    }), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def create_club():
    data = request.get_json()
    club = Club(
        name=data['name'],
        description=data['description'],
        logo_url=data.get('logo_url')
    )
    db.session.add(club)
    db.session.commit()
    
    # Add creator as admin
    membership = ClubMembership(
        user_id=get_jwt_identity(),
        club_id=club.id,
        role='admin'
    )
    db.session.add(membership)
    db.session.commit()
    
    return jsonify({'message': 'Club created successfully', 'id': club.id}), 201

@bp.route('/<int:club_id>/join', methods=['POST'])
@jwt_required()
def join_club(club_id):
    user_id = get_jwt_identity()
    
    # Check if already a member
    if ClubMembership.query.filter_by(user_id=user_id, club_id=club_id).first():
        return jsonify({'error': 'Already a member of this club'}), 400
    
    membership = ClubMembership(
        user_id=user_id,
        club_id=club_id,
        role='member'
    )
    db.session.add(membership)
    db.session.commit()
    
    return jsonify({'message': 'Joined club successfully'}), 201

@bp.route('/<int:club_id>/members', methods=['GET'])
def get_club_members(club_id):
    members = ClubMembership.query.filter_by(club_id=club_id).all()
    return jsonify([{
        'user_id': member.user_id,
        'username': member.member.username,
        'role': member.role,
        'joined_at': member.joined_at.isoformat()
    } for member in members]), 200

@bp.route('/my-clubs', methods=['GET'])
@jwt_required()
def get_my_clubs():
    user_id = get_jwt_identity()
    memberships = ClubMembership.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'club_id': membership.club_id,
        'name': membership.club.name,
        'description': membership.club.description,
        'logo_url': membership.club.logo_url,
        'role': membership.role,
        'joined_at': membership.joined_at.isoformat()
    } for membership in memberships]), 200 