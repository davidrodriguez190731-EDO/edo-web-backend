from database import db
from datetime import datetime


class SiteConfig(db.Model):
    __tablename__ = "site_config"

    id         = db.Column(db.Integer, primary_key=True)
    key        = db.Column(db.String(100), unique=True, nullable=False)
    value      = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "key":        self.key,
            "value":      self.value,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
