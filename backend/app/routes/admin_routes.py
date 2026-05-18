from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, AuditLog, HashHistory
from datetime import datetime, timedelta
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    total_users = User.query.count()
    total_scans = HashHistory.query.count()
    active_users = User.query.filter(User.last_login > datetime.utcnow() - timedelta(days=7)).count()
    
    hash_counts = db.session.query(
        HashHistory.detected_type, 
        db.func.count(HashHistory.detected_type)
    ).group_by(HashHistory.detected_type).all()
    
    daily_scans = []
    for i in range(7):
        day = datetime.utcnow() - timedelta(days=i)
        count = HashHistory.query.filter(
            db.func.date(HashHistory.timestamp) == day.date()
        ).count()
        daily_scans.append({'date': day.date().isoformat(), 'count': count})
    
    api_calls = db.session.query(db.func.sum(User.api_calls_count)).scalar() or 0
    
    return jsonify({
        'total_users': total_users,
        'total_scans': total_scans,
        'active_users': active_users,
        'api_calls': api_calls,
        'top_hashes': [{'type': h[0], 'count': h[1]} for h in hash_counts[:5]],
        'daily_scans': daily_scans
    }), 200

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'role': u.role,
        'created_at': u.created_at.isoformat(),
        'last_login': u.last_login.isoformat() if u.last_login else None,
        'scans_count': len(u.history)
    } for u in users]), 200

@admin_bp.route('/logs', methods=['GET'])
@admin_required
def get_logs():
    limit = request.args.get('limit', 100, type=int)
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
    
    return jsonify([{
        'id': l.id,
        'user_id': l.user_id,
        'action': l.action,
        'ip_address': l.ip_address,
        'details': l.details,
        'timestamp': l.timestamp.isoformat()
    } for l in logs]), 200

@admin_bp.route('/user/<int:user_id>/role', methods=['PUT'])
@admin_required
def update_user_role(user_id):
    data = request.get_json()
    new_role = data.get('role')
    
    if new_role not in ['user', 'premium', 'admin']:
        return jsonify({'error': 'Invalid role'}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user.role = new_role
    db.session.commit()
    
    return jsonify({'message': 'User role updated'}), 200
