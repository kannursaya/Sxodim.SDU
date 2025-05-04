from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Ticket, Event

bp = Blueprint('tickets', __name__)

@bp.route('/', methods=['GET'])
@jwt_required()
def get_user_tickets():
    user_id = get_jwt_identity()
    tickets = Ticket.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': ticket.id,
        'event_id': ticket.event_id,
        'event_title': ticket.event.title,
        'event_date': ticket.event.date.isoformat(),
        'qr_code': ticket.qr_code,
        'status': ticket.status,
        'created_at': ticket.created_at.isoformat()
    } for ticket in tickets]), 200

@bp.route('/<int:ticket_id>', methods=['GET'])
@jwt_required()
def get_ticket(ticket_id):
    user_id = get_jwt_identity()
    ticket = Ticket.query.filter_by(id=ticket_id, user_id=user_id).first_or_404()
    
    return jsonify({
        'id': ticket.id,
        'event_id': ticket.event_id,
        'qr_code': ticket.qr_code,
        'status': ticket.status,
        'created_at': ticket.created_at.isoformat()
    }), 200

@bp.route('/<int:ticket_id>/validate', methods=['POST'])
@jwt_required()
def validate_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    if ticket.status != 'active':
        return jsonify({'error': 'Ticket is not active'}), 400
    
    ticket.status = 'used'
    db.session.commit()
    
    return jsonify({'message': 'Ticket validated successfully'}), 200 