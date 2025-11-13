from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from models import db, Payment
import os
os.environ['FLASK_SKIP_DOTENV'] = '1'
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)


def seed_data():
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


@app.route('/payment', methods=['GET'])
def list_payments():
    ps = Payment.query.all()
    return jsonify([p.to_dict() for p in ps])

@app.route('/health')
def health():
    return jsonify({'status':'ok','service':'payment','time': datetime.utcnow().isoformat()}), 200


@app.route('/payment/<int:pid>', methods=['GET'])
def get_payment(pid):
    p = Payment.query.get(pid)
    if not p:
        return jsonify({'error': 'Payment not found'}), 404
    return jsonify(p.to_dict())


@app.route('/payment', methods=['POST'])
def create_payment():
    data = request.get_json() or {}
    try:
        order_id = int(data.get('order_id', 0))
        amount = int(data.get('amount', 0))
    except Exception:
        return jsonify({'error': 'order_id and amount must be integers'}), 400
    method = data.get('method', '')
    status = data.get('status', 'pending')

    p = Payment(order_id=order_id, amount=amount, method=method, status=status)
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201


@app.route('/payment/<int:pid>', methods=['PUT'])
def update_payment(pid):
    p = Payment.query.get(pid)
    if not p:
        return jsonify({'error': 'Payment not found'}), 404
    data = request.get_json() or {}
    if 'status' in data:
        p.status = data['status']
    if 'amount' in data:
        try:
            p.amount = int(data['amount'])
        except Exception:
            return jsonify({'error': 'amount must be integer'}), 400
    db.session.commit()
    return jsonify(p.to_dict())


@app.route('/payment/<int:pid>', methods=['DELETE'])
def delete_payment(pid):
    p = Payment.query.get(pid)
    if not p:
        return jsonify({'error': 'Payment not found'}), 404
    db.session.delete(p)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(host='127.0.0.1', port=Config.PORT, debug=True)