from datetime import datetime
from . import db

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    total_scored = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<Score {self.total_scored}/{self.total_questions}>'
