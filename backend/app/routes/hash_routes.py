from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, limiter
from app.models import HashHistory, AuditLog
from app.hash_engine import HashIdentifier, BulkHashAnalyzer
import hashlib
import bcrypt
import json

hash_bp = Blueprint('hash', __name__)
hash_identifier = HashIdentifier()
bulk_analyzer = BulkHashAnalyzer(hash_identifier)

@hash_bp.route('/identify', methods=['POST'])
@limiter.limit("30 per minute")
def identify_hash():
    data = request.get_json()
    hash_string = data.get('hash', '').strip()
    
    if not hash_string:
        return jsonify({'error': 'Hash value required'}), 400
    
    results = hash_identifier.identify_hash(hash_string)
    
    # Save to history if authenticated
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            from flask_jwt_extended import decode_token
            token = auth_header.split(' ')[1]
            payload = decode_token(token)
            user_id = payload['sub']
            
            history = HashHistory(
                user_id=user_id,
                hash_value=hash_string,
                detected_type=results[0]['type'] if results else 'unknown',
                confidence=results[0]['confidence'] if results else 0,
                analysis_result=results
            )
            db.session.add(history)
            db.session.commit()
        except:
            pass
    
    return jsonify({
        'hash': hash_string,
        'identifications': results,
        'count': len(results)
    }), 200

@hash_bp.route('/bulk-identify', methods=['POST'])
@limiter.limit("10 per minute")
def bulk_identify():
    data = request.get_json()
    hashes = data.get('hashes', [])
    
    if not hashes:
        return jsonify({'error': 'No hashes provided'}), 400
    
    results = bulk_analyzer.analyze_bulk(hashes)
    
    return jsonify(results), 200

@hash_bp.route('/generate', methods=['POST'])
@limiter.limit("60 per minute")
def generate_hash():
    data = request.get_json()
    text = data.get('text', '')
    algorithm = data.get('algorithm', 'sha256')
    salt = data.get('salt', '')
    
    if not text:
        return jsonify({'error': 'Text required'}), 400
    
    result = {}
    
    if algorithm == 'md5':
        result['hash'] = hashlib.md5(text.encode()).hexdigest()
    elif algorithm == 'sha1':
        result['hash'] = hashlib.sha1(text.encode()).hexdigest()
    elif algorithm == 'sha256':
        result['hash'] = hashlib.sha256(text.encode()).hexdigest()
    elif algorithm == 'sha512':
        result['hash'] = hashlib.sha512(text.encode()).hexdigest()
    elif algorithm == 'bcrypt':
        salt_bytes = bcrypt.gensalt()
        result['hash'] = bcrypt.hashpw(text.encode(), salt_bytes).decode()
    else:
        return jsonify({'error': 'Unsupported algorithm'}), 400
    
    if salt:
        salted_text = salt + text
        result['salted_hash'] = hashlib.sha256(salted_text.encode()).hexdigest()
        result['salt'] = salt
    
    result['algorithm'] = algorithm
    result['input'] = text
    
    return jsonify(result), 200

@hash_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    history = HashHistory.query.filter_by(user_id=user_id).order_by(HashHistory.timestamp.desc()).limit(100).all()
    
    return jsonify([{
        'id': h.id,
        'hash': h.hash_value,
        'type': h.detected_type,
        'confidence': h.confidence,
        'timestamp': h.timestamp.isoformat(),
        'is_favorite': h.is_favorite
    } for h in history]), 200

@hash_bp.route('/favorite/<int:history_id>', methods=['POST'])
@jwt_required()
def toggle_favorite(history_id):
    user_id = get_jwt_identity()
    history = HashHistory.query.filter_by(id=history_id, user_id=user_id).first()
    
    if not history:
        return jsonify({'error': 'History entry not found'}), 404
    
    history.is_favorite = not history.is_favorite
    db.session.commit()
    
    return jsonify({'is_favorite': history.is_favorite}), 200
