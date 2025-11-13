from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from models import db, Restoran
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)


def seed_data():
    if not Restoran.query.first():
        samples = [
            Restoran(name='Warung Asri', address='Jl. Merdeka 123', phone='081234567890'),
            Restoran(name='Restoran Tiga Rasa', address='Jl. Sudirman 456', phone='081298765432'),
        ]
        db.session.add_all(samples)
        db.session.commit()


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


@app.route('/restoran', methods=['GET'])
def list_restoran():
    restos = Restoran.query.all()
    return jsonify([r.to_dict() for r in restos])


@app.route('/restoran/<int:rid>', methods=['GET'])
def get_resto(rid):
    r = Restoran.query.get(rid)
    if not r:
        return jsonify({'error': 'Restaurant not found'}), 404
    return jsonify(r.to_dict())


@app.route('/restoran', methods=['POST'])
def create_resto():
    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'error': 'name is required'}), 400
    r = Restoran(
        name=name,
        address=data.get('address'),
        phone=data.get('phone')
    )
    db.session.add(r)
    db.session.commit()
    return jsonify(r.to_dict()), 201


@app.route('/restoran/<int:rid>', methods=['PUT'])
def update_resto(rid):
    r = Restoran.query.get(rid)
    if not r:
        return jsonify({'error': 'Restaurant not found'}), 404
    data = request.get_json() or {}
    if 'name' in data and data['name']:
        r.name = data['name']
    if 'address' in data:
        r.address = data['address']
    if 'phone' in data:
        r.phone = data['phone']
    db.session.commit()
    return jsonify(r.to_dict())


@app.route('/restoran/<int:rid>', methods=['DELETE'])
def delete_resto(rid):
    r = Restoran.query.get(rid)
    if not r:
        return jsonify({'error': 'Restaurant not found'}), 404
    db.session.delete(r)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(host='127.0.0.1', port=Config.PORT, debug=True)