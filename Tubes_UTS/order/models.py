from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    # items stored as JSON text: [{"item_id":1,"qty":2,"price":25000}, ...]
    items = db.Column(db.Text, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending/confirmed/completed/cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def parsed_items(self):
        try:
            return json.loads(self.items)
        except Exception:
            return []

    def to_dict(self):
        return {
            'id': self.id,
            'items': self.parsed_items(),
            'total_price': self.total_price,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Order {self.id} total={self.total_price} status={self.status}>'