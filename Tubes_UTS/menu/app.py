from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from models import db, Menu as MenuModel, Restoran as RestoranModel
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)


def seed_data():
    """Isi data awal jika tabel masih kosong"""
    if not RestoranModel.query.first():
        restos = [
            RestoranModel(name='Warung Asri', address='Jl. Merdeka 123'),
            RestoranModel(name='Restoran Tiga Rasa', address='Jl. Sudirman 456'),
        ]
        db.session.add_all(restos)

    if not MenuModel.query.first():
        menus = [
            MenuModel(name='Nasi Goreng', price=25000, description='Nasi goreng spesial', image_url='/static/img/nasi-goreng.jpg'),
            MenuModel(name='Soto Ayam', price=18000, description='Soto ayam tradisional', image_url='/static/img/soto-ayam.jpg'),
            MenuModel(name='Gado-gado', price=15000, description='Gado-gado saus kacang', image_url='/static/img/gado-gado.jpg'),
        ]
        db.session.add_all(menus)

    db.session.commit()


try:
    @app.before_first_request
    def create_tables_and_seed():
        db.create_all()
        seed_data()
except Exception:
    def create_tables_and_seed():
        db.create_all()
        seed_data()


@app.route('/items', methods=['GET'])
def list_items():
    items = MenuModel.query.all()
    return jsonify([m.to_dict() for m in items])


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    m = MenuModel.query.get(item_id)
    if not m:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(m.to_dict())


@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    price = data.get('price', 0)
    try:
        price = int(price)
    except Exception:
        return jsonify({'error': 'price must be an integer'}), 400
    description = data.get('description', '')
    image_url = data.get('image_url', '')
    restoran_id = data.get('restoran_id', None)

    item = MenuModel(name=name, price=price, description=description, image_url=image_url, restoran_id=restoran_id)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    m = MenuModel.query.get(item_id)
    if not m:
        return jsonify({'error': 'Item not found'}), 404
    data = request.get_json() or {}
    if 'name' in data:
        m.name = data['name']
    if 'price' in data:
        try:
            m.price = int(data['price'])
        except Exception:
            return jsonify({'error': 'price must be an integer'}), 400
    if 'description' in data:
        m.description = data['description']
    if 'image_url' in data:
        m.image_url = data['image_url']
    if 'restoran_id' in data:
        m.restoran_id = data['restoran_id']
    db.session.commit()
    return jsonify(m.to_dict())


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    m = MenuModel.query.get(item_id)
    if not m:
        return jsonify({'error': 'Item not found'}), 404
    db.session.delete(m)
    db.session.commit()
    return '', 204


@app.route('/restoran', methods=['GET'])
def list_restoran():
    restos = RestoranModel.query.all()
    return jsonify([r.to_dict() for r in restos])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(host='127.0.0.1', port=Config.PORT, debug=True)