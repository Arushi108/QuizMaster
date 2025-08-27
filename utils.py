from werkzeug.security import generate_password_hash
from models import db
from models.user import User

def create_admin():
    """Create default admin user if not exists"""
    admin = User.query.filter_by(username='admin@quizmaster.com').first()
    if not admin:
        admin = User(
            username='admin@quizmaster.com',
            password_hash=generate_password_hash('admin123'),
            full_name='Quiz Master Admin',
            qualification='Administrator',
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin@quizmaster.com / admin123")
