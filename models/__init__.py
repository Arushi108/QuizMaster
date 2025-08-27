from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_models():
    """Initialize all models - call this after db is configured"""
    from .user import User
    from .subject import Subject  
    from .chapter import Chapter
    from .quiz import Quiz
    from .question import Question
    from .score import Score
    
    return User, Subject, Chapter, Quiz, Question, Score
