from datetime import datetime
from . import db

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Chapter {self.name}>'
