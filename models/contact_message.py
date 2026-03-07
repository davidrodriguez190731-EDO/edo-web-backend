from database import db
from datetime import datetime

class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(150))
    company    = db.Column(db.String(150))
    email      = db.Column(db.String(150))
    project_type = db.Column(db.String(100))
    message    = db.Column(db.Text)
    read       = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "company":     self.company,
            "email":       self.email,
            "projectType": self.project_type,
            "message":     self.message,
            "read":        self.read,
            "date":        self.created_at.strftime("%Y-%m-%d %H:%M") if self.created_at else "",
        }
