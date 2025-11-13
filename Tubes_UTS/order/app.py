from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json
from models import db, Order
import os
os.environ['FLASK_SKIP_DOTENV'] = '1'
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)


def seed_data():
    # nothing required beyond create_database.py seed, kept for parity
    pass


# safe decorator usage; also call manually in __main__
try:
    @app.before_first_request
    def create_tables_and_seed():
        db.create_all()
        seed_data()
except Exception:
    def create_tables_and_seed():
        db.create_all()
        seed_data()


@app.route('/orders', methods=['GET'])
def list_orders():
    orders = Order.query.all()
    return jsonify([o.to_dict() for o in orders])

@app.route('/health')
def health():
    return jsonify({'status':'ok','service':'order','time': datetime.utcnow().isoformat()}), 200


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    o = Order.query.get(order_id)
    if not o:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(o.to_dict())


@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json() or {}
    items = data.get('items', [])
    if not isinstance(items, list) or len(items) == 0:
        return jsonify({'error': 'items must be a non-empty list'}), 400
    try:
        total_price = int(data.get('total_price', 0))
    except Exception:
        return jsonify({'error': 'total_price must be integer'}), 400

    o = Order(items=json.dumps(items), total_price=total_price, status=data.get('status', 'pending'))
    db.session.add(o)
    db.session.commit()
    return jsonify(o.to_dict()), 201


@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    o = Order.query.get(order_id)
    if not o:
        return jsonify({'error': 'Order not found'}), 404
    data = request.get_json() or {}
    if 'items' in data:
        if not isinstance(data['items'], list):
            return jsonify({'error': 'items must be a list'}), 400
        o.items = json.dumps(data['items'])
    if 'total_price' in data:
        try:
            o.total_price = int(data['total_price'])
        except Exception:
            return jsonify({'error': 'total_price must be integer'}), 400
    if 'status' in data:
        o.status = data['status']
    db.session.commit()
    return jsonify(o.to_dict())


@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    o = Order.query.get(order_id)
    if not o:
        return jsonify({'error': 'Order not found'}), 404
    db.session.delete(o)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(host='127.0.0.1', port=Config.PORT, debug=True)