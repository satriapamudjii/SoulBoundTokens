from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

db = SQLAlchemy(app)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_value = db.Column(db.String(256), nullable=False)
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
    data = request.json
    token = Token(token_value=data['token'], owner_id=data['owner_id'])
    db.session.add(token)
    db.session.commit()
    return jsonify({'message': 'Token issued successfully', 'data': token.serialize()}), 201

@token_bp.route('/<int:token_id>', methods=['GET'])
def get_token(token_id):
    token = Token.query.get_or_404(token_id)
    return jsonify(token.serialize())

@token_bp.route('/<int:token_id>', methods=['PUT'])
def update_token(token_id):
    data = request.json
    token = Token.query.get_or_404(token_id)
    token.token_value = data['token']
    db.session.commit()
    return jsonify({'message': 'Token updated successfully', 'data': token.serialize()})

@token_bp.route('/<int:token_id>', methods=['DELETE'])
def delete_token(token_id):
    token = Token.query.get_or_404(token_id)
    db.session.delete(token)
    db.session.commit()
    return jsonify({'message': 'Token deleted successfully'})

@token_bp.route('/verify/<int:owner_id>', methods=['GET'])
def verify_token(owner_id):
    tokens = Token.query.filter_by(owner_id=owner_id).all()
    if not tokens:
        return jsonify({'message': 'No tokens found for the given owner'}), 404
    return jsonify({'message': 'Token(s) found', 'data': [token.serialize() for token in tokens]})

app.register_blueprint(token_bp)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)