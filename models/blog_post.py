from database import db
from datetime import datetime

class BlogPost(db.Model):
    __tablename__ = "blog_posts"

    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(300), nullable=False)
    excerpt    = db.Column(db.Text)
    content    = db.Column(db.Text)
    category   = db.Column(db.String(80))
    read_time  = db.Column(db.String(20), default="5 min")
    published  = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id":        self.id,
            "title":     self.title,
            "excerpt":   self.excerpt,
            "content":   self.content,
            "category":  self.category,
            "readTime":  self.read_time,
            "published": self.published,
            "date":      self.created_at.strftime("%Y-%m-%d") if self.created_at else "",
        }
