from datetime import datetime
from . import db

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Subject {self.name}>'
