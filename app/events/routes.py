from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Event, Ticket, User
import qrcode
import os
from datetime import datetime

bp = Blueprint('events', __name__)

@bp.route('/', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'date': event.date.isoformat(),
        'location': event.location,
        'capacity': event.capacity,
        'image_url': event.image_url,
        'tickets_sold': event.tickets.count()
    } for event in events]), 200

@bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify({
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'date': event.date.isoformat(),
        'location': event.location,
        'capacity': event.capacity,
        'image_url': event.image_url,
        'tickets_sold': event.tickets.count()
    }), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def create_event():
    data = request.get_json()
    event = Event(
        title=data['title'],
        description=data['description'],
        date=datetime.fromisoformat(data['date']),
        location=data['location'],
        capacity=data['capacity'],
        image_url=data.get('image_url')
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully', 'id': event.id}), 201

@bp.route('/<int:event_id>/tickets', methods=['POST'])
@jwt_required()
def purchase_ticket(event_id):
    user_id = get_jwt_identity()
    event = Event.query.get_or_404(event_id)
    
    if event.tickets.count() >= event.capacity:
        return jsonify({'error': 'Event is full'}), 400
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr_data = f"event:{event_id},user:{user_id},timestamp:{datetime.utcnow().timestamp()}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Save QR code
    qr_filename = f"ticket_{event_id}_{user_id}.png"
    qr_path = os.path.join('uploads', qr_filename)
    qr.make_image(fill_color="black", back_color="white").save(qr_path)
    
    ticket = Ticket(
        user_id=user_id,
        event_id=event_id,
        qr_code=qr_path
    )
    
    db.session.add(ticket)
    db.session.commit()
    
    return jsonify({
        'message': 'Ticket purchased successfully',
        'ticket_id': ticket.id,
        'qr_code': qr_path
    }), 201

@bp.route('/tickets/<int:ticket_id>', methods=['GET'])
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

@bp.route('/tickets', methods=['GET'])
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