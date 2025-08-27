from datetime import datetime
from . import db

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')
    scores = db.relationship('Score', backref='quiz', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Quiz for {self.chapter.name}>'
