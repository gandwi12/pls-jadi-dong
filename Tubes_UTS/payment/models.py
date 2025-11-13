from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False) 
    amount = db.Column(db.Integer, nullable=False)
    method = db.Column(db.String(100))
    status = db.Column(db.String(50), default='pending') 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'amount': self.amount,
            'method': self.method,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Payment {self.id} order:{self.order_id} amount:{self.amount}>'