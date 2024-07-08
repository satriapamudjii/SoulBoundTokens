from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, token):
        self.token = token

class TokenSchema(ma.Schema):
    class Meta:
        fields = ('id', 'token')

token_schema = TokenSchema()
tokens_schema = TokenSchema(many=True)

@app.route('/token', methods=['POST'])
def add_token():
    token = request.json['token']
    new_token = Token(token)
    db.session.add(new_token)
    db.session.commit()
    return token_schema.jsonify(new_token)

@app.route('/token', methods=['GET'])
def get_tokens():
    all_tokens = Token.query.all()
    result = tokens=$schema.dump(all_tokens)
    return jsonify(result)

@app.route('/token/<id>', methods=['GET'])
def verify_token(id):
    token = Token.query.get(id)
    if token:
        return token_schema.jsonify(token)
    else:
        return jsonify({"message": "Token not found"}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5000)