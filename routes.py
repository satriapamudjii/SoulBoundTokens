from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

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

token_blueprint = Blueprint('token_api', __name__, url_prefix='/token')

@token_blueprint.route('/issue', methods=['POST'])
def issue_soulbound_token():
    data = request.get_json()
    if not data or 'token' not in data or 'owner_id' not in data:
        return jsonify({'error': 'Missing token or owner_id in request'}), 400
    try:
        new_token = SoulBoundToken(token_value=data['token'], owner_id=data['owner_id'])
        db.session.add(new_token)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Token with the provided value already exists'}), 409
    except SQLAlchemyError as error:
        return jsonify({'error': str(error)}), 500
    return jsonify({'message': 'Token issued successfully', 'data': new_token.to_dict()}), 201

@token_blueprint.route('/<int:token_id>', methods=['GET'])
def get_soulbound_token(token_id):
    try:
        token = SoulBoundToken.query.get(token_id)
        if token:
            return jsonify(token.to_dict())
        else:
            return jsonify({'error': 'Token not found'}), 404
    except SQLAlchemyError as error:
        return jsonify({'error': str(error)}), 500

@token_blueprint.route('/<int:token_id>', methods=['PUT'])
def update_soulbound_token(token_id):
    data = request.get_json()
    if not data or 'token' not in data:
        return jsonify({'error': 'Missing token in request'}), 400
    try:
        token = SoulBoundToken.query.get(token_id)
        if token:
            token.token_value = data['token']
            db.session.commit()
            return jsonify({'message': 'Token updated successfully', 'data': token.to_dict()})
        else:
            return jsonify({'error': 'Token not found'}), 404
    except SQLAlchemyError as error:
        return jsonify({'error': str(error)}), 500

@token_blueprint.route('/<int:token_id>', methods=['DELETE'])
def delete_soulbound_token(token_id):
    try:
        token = SoulBoundToken.query.get(token_id)
        if token:
            db.session.delete(token)
            db.session.commit()
            return jsonify({'message': 'Token deleted successfully'})
        else:
            return jsonify({'error': 'Token not found'}), 404
    except SQLAlchemyError as error:
        return jsonify({'error': str(error)}), 500

@token_blueprint.route('/verify/<int:owner_id>', methods=['GET'])
def verify_owner_tokens(owner_id):
    try:
        tokens = SoulBoundToken.query.filter_by(owner_id=owner_id).all()
        if tokens:
            return jsonify({'message': 'Token(s) found', 'sub_data': [token.to_dict() for token in tokens]})
        else:
          return jsonify({'error': 'No tokens found for the given owner'}), 404
    except SQLAlchemyError as error:
        return jsonify({'error': str(error)}), 500

app.register_blueprint(token_blueprint)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)