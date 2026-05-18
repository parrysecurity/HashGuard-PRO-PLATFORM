from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, limiter
from app.models import ApiKey, AuditLog, User
from app.hash_engine import HashIdentifier
import uuid
from datetime import datetime

api_bp = Blueprint('api', __name__)
hash_identifier = HashIdentifier()

@api_bp.route('/keys', methods=['POST'])
@jwt_required()
def create_api_key():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    api_key = ApiKey(
        user_id=user_id,
        name=data.get('name', 'Default Key'),
        rate_limit=data.get('rate_limit', 100)
    )
    
    db.session.add(api_key)
    db.session.commit()
    
    return jsonify({
        'api_key': api_key.api_key,
        'name': api_key.name,
        'rate_limit': api_key.rate_limit
    }), 201

@api_bp.route('/keys', methods=['GET'])
@jwt_required()
def get_api_keys():
    user_id = get_jwt_identity()
    keys = ApiKey.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': k.id,
        'name': k.name,
        'api_key': k.api_key,
        'rate_limit': k.rate_limit,
        'created_at': k.created_at.isoformat(),
        'last_used': k.last_used.isoformat() if k.last_used else None,
        'is_active': k.is_active
    } for k in keys]), 200

@api_bp.route('/identify', methods=['POST'])
def public_identify():
    data = request.get_json()
    api_key = request.headers.get('X-API-Key')
    
    if api_key:
        key = ApiKey.query.filter_by(api_key=api_key, is_active=True).first()
        if key:
            key.last_used = datetime.utcnow()
            db.session.commit()
            
            user = User.query.get(key.user_id)
            if user:
                user.api_calls_count += 1
                db.session.commit()
        else:
            return jsonify({'error': 'Invalid API key'}), 401
    
    hash_string = data.get('hash', '').strip()
    if not hash_string:
        return jsonify({'error': 'Hash value required'}), 400
    
    results = hash_identifier.identify_hash(hash_string)
    
    return jsonify({
        'hash': hash_string,
        'identifications': results,
        'count': len(results)
    }), 200

@api_bp.route('/swagger.json', methods=['GET'])
def swagger_spec():
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "Hash Identifier API",
            "version": "1.0.0",
            "description": "Cryptographic hash identification service"
        },
        "servers": [
            {"url": "http://localhost/api", "description": "Local server"}
        ],
        "paths": {
            "/identify": {
                "post": {
                    "summary": "Identify hash type",
                    "parameters": [
                        {
                            "name": "X-API-Key",
                            "in": "header",
                            "schema": {"type": "string"}
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "hash": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Success"}
                    }
                }
            }
        }
    })
