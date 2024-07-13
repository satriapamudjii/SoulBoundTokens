from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

db = SQLAlchemy(app)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_value = db.Column(db.String(256), nullable=False, unique=True)
    owner_id = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'token_value': self.token_value,
            'owner_id': self.owner_id
        }

token_bp = Blueprint('token_api', __name__, url_prefix='/token')

@token_bp.route('/issue', methods=['POST'])
def issue_token():
    data = request.get_json()
    if not data or 'token' not in data or 'owner_id' not in data:
        return jsonify({'error': 'Missing token or owner_id in request'}), 400
    try:
        token = Token(token_value=data['token'], owner_id=data['owner_id'])
        db.session.add(token)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Token with the provided value already exists'}), 409
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'message': 'Token issued successfully', 'data': token.serialize()}), 201

@token_bp.route('/<int:token_id>', methods=['GET'])
def get_token(token_id):
    try:
        token = Token.query.get(token_id)
        if token:
            return jsonify(token.serialize())
        else:
            return jsonify({'error': 'Token not found'}), 404
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@token_bp.route('/<int:token_id>', methods=['PUT'])
def update_token(token_id):
    data = request.get_json()
    if not data or 'token' not in data:
        return jsonify({'error': 'Missing token in request'}), 400
    try:
        token = Token.query.get(token_id)
        if token:
            token.token_value = data['token']
            db.session.commit()
            return jsonify({'message': 'Token updated successfully', 'data': token.serialize()})
        else:
            return jsonify({'error': 'Token not found'}), 404
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@token_bp.route('/<int:token_id>', methods=['DELETE'])
def delete_token(token_id):
    try:
        token = Token.query.get(token_id)
        if token:
            db.session.delete(token)
            db.session.commit()
            return jsonify({'message': 'Token deleted successfully'})
        else:
            return jsonify({'error': 'Token not found'}), 404
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@token_bp.route('/verify/<int:owner_id>', methods=['GET'])
def verify_token(owner_id):
    try:
        tokens = Token.query.filter_by(owner_id=owner_id).all()
        if tokens:
            return jsonify({'message': 'Token(s) found', 'data': [token.serialize() for token in tokens]})
        else:
            return jsonify({'error': 'No tokens found for the given owner'}), 404
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

app.register_blueprint(token_bp)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)