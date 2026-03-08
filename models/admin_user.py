from database import db
from datetime import datetime

class AdminUser(db.Model):
    __tablename__ = "admin_users"
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=True)
    full_name     = db.Column(db.String(120), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active     = db.Column(db.Boolean, default=True, nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "username":   self.username,
            "email":      self.email or '',
            "full_name":  self.full_name or '',
            "is_active":  self.is_active,
            "created_at": self.created_at.strftime('%d/%m/%Y') if self.created_at else ''
        }
