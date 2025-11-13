from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from models import db, User, Transaction
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)


def seed_data():
    # db.create_all() will have been called in __main__ when run directly
    pass


try:
    @app.before_first_request
    def create_tables_and_seed():
        db.create_all()
        seed_data()
except Exception:
    def create_tables_and_seed():
        db.create_all()
        seed_data()


# Users
@app.route('/users', methods=['GET'])
def list_users():
    return jsonify([u.to_dict() for u in User.query.all()])


@app.route('/users/<int:uid>', methods=['GET'])
def get_user(uid):
    u = User.query.get(uid)
    if not u:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(u.to_dict(include_transactions=True))


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    password = data.get('password') or ''
    if not name or not email or not password:
        return jsonify({'error': 'name, email, password required'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'email already used'}), 400
    u = User(name=name, email=email, password=password)
    db.session.add(u)
    db.session.commit()
    return jsonify(u.to_dict()), 201


@app.route('/users/<int:uid>', methods=['PUT'])
def update_user(uid):
    u = User.query.get(uid)
    if not u:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json() or {}
    if 'name' in data:
        u.name = data['name']
    if 'password' in data:
        u.password = data['password']
    if 'balance' in data:
        try:
            u.balance = float(data['balance'])
        except Exception:
            return jsonify({'error': 'balance must be number'}), 400
    db.session.commit()
    return jsonify(u.to_dict())


@app.route('/users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    u = User.query.get(uid)
    if not u:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(u)
    db.session.commit()
    return '', 204


# Transactions
@app.route('/users/<int:uid>/transactions', methods=['GET'])
def list_transactions(uid):
    u = User.query.get(uid)
    if not u:
        return jsonify({'error': 'User not found'}), 404
    return jsonify([t.to_dict() for t in u.transactions])


@app.route('/users/<int:uid>/transactions', methods=['POST'])
def create_transaction(uid):
    u = User.query.get(uid)
    if not u:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json() or {}
    try:
        amount = float(data.get('amount', 0))
    except Exception:
        return jsonify({'error': 'amount must be number'}), 400
    ttype = data.get('type') or 'credit'
    desc = data.get('description') or ''
    tx = Transaction(user_id=uid, amount=amount, type=ttype, description=desc)
    # update user balance
    if ttype == 'credit':
        u.balance += amount
    elif ttype == 'debit':
        u.balance -= amount
    db.session.add(tx)
    db.session.commit()
    return jsonify(tx.to_dict()), 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=Config.PORT, debug=True)