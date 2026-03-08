from database import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = "projects"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(200), nullable=False)
    category    = db.Column(db.String(100))
    status      = db.Column(db.String(50), default="En producción")
    description = db.Column(db.Text)
    highlights  = db.Column(db.Text)       # "item1|item2|item3"
    color       = db.Column(db.String(20), default="#1B4B8A")
    featured    = db.Column(db.Boolean, default=False)
    order       = db.Column(db.Integer, default=99)
    visible     = db.Column(db.Boolean, default=True)
    # ── Imágenes (base64 o URL) separadas por | ──────────────────
    images      = db.Column(db.Text)       # "url1|url2|url3"
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "category":    self.category,
            "status":      self.status,
            "description": self.description,
            "highlights":  self.highlights.split("|") if self.highlights else [],
            "color":       self.color,
            "featured":    self.featured,
            "order":       self.order,
            "visible":     self.visible,
            "images":      self.images.split("|") if self.images else [],
        }
