from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db = SQLAlchemy(app)

class SoulBoundToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_value = db.Column(db.String(256), nullable=False, unique=True)
    owner_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'token_value': self.token_value,
            'owner_id': self.owner_id
        }

def required_fields_checker(data, fields):
    return all(field in data for field in fields)

@app.errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(error):
    db.session.rollback()
    return jsonify({'error': 'Database error', 'message': str(error)}), 500

token_blueprint = Blueprint('token_api', __name__, url_prefix='/token')

@token_blueprint.route('/issue', methods=['POST'])
def issue_soulbound_token():
    data = request.get_json()
    if not data or not required_fields_checker(data, ['token', 'owner_id']):
        return jsonify({'error': 'Missing token or owner_id in request'}), 400
    try:
        new_token = SoulBoundToken(token_value=data['token'], owner_id=data['owner_id'])
        db.session.add(new_token)
        db.session.commit()
        return jsonify({'message': 'Token issued successfully', 'data': new_token.to_dict()}), 201
    except IntegrityError:
        return jsonify({'error': 'Token with the provided value already exists'}), 409

@token_blueprint.route('/<int:token_id>', methods=['GET'])
def get_soulbound_token(token_id):
    token = SoulBoundToken.query.get(token_id)
    if token:
        return jsonify(token.to_dict())
    return jsonify({'error': 'Token not found'}), 404

@token_blueprint.route('/<int:token_id>', methods=['PUT'])
def update_soulbound_token(token_id):
    data = request.get_json()
    if not data or 'token' not in data:
        return jsonify({'error': 'Missing token in request'}), 400
    token = SoulBoundToken.query.get(token_id)
    if token:
        token.token_value = data['token']
        db.session.commit()
        return jsonify({'message': 'Token updated successfully', 'data': token.to_dict()})
    return jsonify({'error': 'Token not found'}), 404

@token_blueprint.route('/<int:token_id>', methods=['DELETE'])
def delete_soulbound_token(token_id):
    token = SoulBoundToken.query.get(token_id)
    if token:
        db.session.delete(token)
        db.session.commit()
        return jsonify({'message': 'Token deleted successfully'})
    return jsonify({'error': 'Token not found'}), 404

@token_blueprint.route('/verify/<int:owner_id>', methods=['GET'])
def verify_owner_tokens(owner_id):
    tokens = SoulBoundToken.query.filter_by(owner_id=owner_id).all()
    if tokens:
        return jsonify({'message': 'Token(s) found', 'data': [token.to_dict() for token in tokens]})
    return jsonify({'error': 'No tokens found for the given owner'}), 404

app.register_blueprint(token_blueprint)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)