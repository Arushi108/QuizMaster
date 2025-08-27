#!/usr/bin/env python3
"""
Database Setup Script for Quiz Master Application
This script initializes the database and populates it with sample data.
"""

from app import create_app
from models import db
from models.user import User
from models.subject import Subject
from models.chapter import Chapter
from models.quiz import Quiz
from models.question import Question
from models.score import Score
from werkzeug.security import generate_password_hash
from datetime import datetime, date
import sys

app = create_app()

def create_database():
    """Create all database tables"""
    print("Creating database tables...")
    with app.app_context():
        db.create_all()
        print("✓ Database tables created successfully")

def create_admin_user():
    """Create the default admin user"""
    print("Creating admin user...")
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(username='admin@quizmaster.com').first()
        if not admin:
            admin = User(
                username='admin@quizmaster.com',
                password_hash=generate_password_hash('admin123'),
                full_name='Quiz Master Admin',
                qualification='Administrator',
                is_admin=True,
                dob=date(1990, 1, 1)
            )
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created successfully")
            print("  Email: admin@quizmaster.com")
            print("  Password: admin123")
        else:
            print("✓ Admin user already exists")

def create_sample_users():
    """Create sample regular users"""
    print("Creating sample users...")
    with app.app_context():
        sample_users = [
            {
                'username': 'john.doe@example.com',
                'password': 'password123',
                'full_name': 'John Doe',
                'qualification': 'Bachelor of Science',
                'dob': date(1995, 5, 15)
            },
            {
                'username': 'jane.smith@example.com',
                'password': 'password123',
                'full_name': 'Jane Smith',
                'qualification': 'Master of Arts',
                'dob': date(1993, 8, 22)
            },
            {
                'username': 'student@example.com',
                'password': 'student123',
                'full_name': 'Test Student',
                'qualification': 'High School',
                'dob': date(2000, 3, 10)
            }
        ]
        
        for user_data in sample_users:
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if not existing_user:
                user = User(
                    username=user_data['username'],
                    password_hash=generate_password_hash(user_data['password']),
                    full_name=user_data['full_name'],
                    qualification=user_data['qualification'],
                    dob=user_data['dob'],
                    is_admin=False
                )
                db.session.add(user)
        
        db.session.commit()
        print(f"✓ Sample users created successfully")

def create_sample_subjects():
    """Create sample subjects"""
    print("Creating sample subjects...")
    with app.app_context():
        subjects_data = [
            {
                'name': 'Mathematics',
                'description': 'Comprehensive mathematics covering algebra, geometry, calculus, and statistics.'
            },
            {
                'name': 'Science',
                'description': 'General science including physics, chemistry, and biology concepts.'
            },
            {
                'name': 'History',
                'description': 'World history covering ancient civilizations to modern times.'
            },
            {
                'name': 'English Literature',
                'description': 'English literature, grammar, and comprehension skills.'
            },
            {
                'name': 'Computer Science',
                'description': 'Programming, algorithms, data structures, and computer fundamentals.'
            }
        ]
        
        for subject_data in subjects_data:
            existing_subject = Subject.query.filter_by(name=subject_data['name']).first()
            if not existing_subject:
                subject = Subject(
                    name=subject_data['name'],
                    description=subject_data['description']
                )
                db.session.add(subject)
        
        db.session.commit()
        print(f"✓ {len(subjects_data)} subjects created successfully")

def create_sample_chapters():
    """Create sample chapters for subjects"""
    print("Creating sample chapters...")
    with app.app_context():
        # Mathematics chapters
        math_subject = Subject.query.filter_by(name='Mathematics').first()
        if math_subject:
            math_chapters = [
                {'name': 'Algebra Basics', 'description': 'Linear equations, quadratic equations, and polynomials'},
                {'name': 'Geometry', 'description': 'Shapes, angles, area, and volume calculations'},
                {'name': 'Calculus', 'description': 'Derivatives, integrals, and limits'},
                {'name': 'Statistics', 'description': 'Mean, median, mode, and probability'}
            ]
            for chapter_data in math_chapters:
                existing_chapter = Chapter.query.filter_by(name=chapter_data['name'], subject_id=math_subject.id).first()
                if not existing_chapter:
                    chapter = Chapter(
                        name=chapter_data['name'],
                        description=chapter_data['description'],
                        subject_id=math_subject.id
                    )
                    db.session.add(chapter)
        
        # Science chapters
        science_subject = Subject.query.filter_by(name='Science').first()
        if science_subject:
            science_chapters = [
                {'name': 'Physics Fundamentals', 'description': 'Motion, force, energy, and waves'},
                {'name': 'Chemistry Basics', 'description': 'Atoms, molecules, and chemical reactions'},
                {'name': 'Biology Introduction', 'description': 'Cell structure, genetics, and evolution'},
                {'name': 'Earth Science', 'description': 'Geology, weather, and environmental science'}
            ]
            for chapter_data in science_chapters:
                existing_chapter = Chapter.query.filter_by(name=chapter_data['name'], subject_id=science_subject.id).first()
                if not existing_chapter:
                    chapter = Chapter(
                        name=chapter_data['name'],
                        description=chapter_data['description'],
                        subject_id=science_subject.id
                    )
                    db.session.add(chapter)
        
        # Computer Science chapters
        cs_subject = Subject.query.filter_by(name='Computer Science').first()
        if cs_subject:
            cs_chapters = [
                {'name': 'Programming Basics', 'description': 'Variables, loops, and functions'},
                {'name': 'Data Structures', 'description': 'Arrays, lists, stacks, and queues'},
                {'name': 'Algorithms', 'description': 'Sorting, searching, and optimization'},
                {'name': 'Web Development', 'description': 'HTML, CSS, JavaScript, and frameworks'}
            ]
            for chapter_data in cs_chapters:
                existing_chapter = Chapter.query.filter_by(name=chapter_data['name'], subject_id=cs_subject.id).first()
                if not existing_chapter:
                    chapter = Chapter(
                        name=chapter_data['name'],
                        description=chapter_data['description'],
                        subject_id=cs_subject.id
                    )
                    db.session.add(chapter)
        
        db.session.commit()
        print("✓ Sample chapters created successfully")

def create_sample_quiz():
    """Create a sample quiz with questions"""
    print("Creating sample quiz...")
    with app.app_context():
        # Get the first chapter (Algebra Basics)
        algebra_chapter = Chapter.query.filter_by(name='Algebra Basics').first()
        if algebra_chapter:
            # Create a quiz
            existing_quiz = Quiz.query.filter_by(chapter_id=algebra_chapter.id).first()
            if not existing_quiz:
                quiz = Quiz(
                    chapter_id=algebra_chapter.id,
                    date_of_quiz=date.today(),
                    time_duration=30,  # 30 minutes
                    remarks='Basic algebra assessment'
                )
                db.session.add(quiz)
                db.session.commit()
                
                # Add sample questions
                questions_data = [
                    {
                        'question_statement': 'What is the value of x in the equation: 2x + 5 = 13?',
                        'option1': 'x = 3',
                        'option2': 'x = 4',
                        'option3': 'x = 5',
                        'option4': 'x = 6',
                        'correct_option': 2
                    },
                    {
                        'question_statement': 'Simplify: 3x + 7x',
                        'option1': '10x',
                        'option2': '21x',
                        'option3': '10x²',
                        'option4': '4x',
                        'correct_option': 1
                    },
                    {
                        'question_statement': 'What is the slope of the line y = 2x + 3?',
                        'option1': '2',
                        'option2': '3',
                        'option3': '2x',
                        'option4': '5',
                        'correct_option': 1
                    },
                    {
                        'question_statement': 'Factor: x² - 9',
                        'option1': '(x - 3)(x - 3)',
                        'option2': '(x + 3)(x + 3)',
                        'option3': '(x + 3)(x - 3)',
                        'option4': 'Cannot be factored',
                        'correct_option': 3
                    },
                    {
                        'question_statement': 'If f(x) = 2x + 1, what is f(5)?',
                        'option1': '10',
                        'option2': '11',
                        'option3': '12',
                        'option4': '9',
                        'correct_option': 2
                    }
                ]
                
                for question_data in questions_data:
                    question = Question(
                        quiz_id=quiz.id,
                        question_statement=question_data['question_statement'],
                        option1=question_data['option1'],
                        option2=question_data['option2'],
                        option3=question_data['option3'],
                        option4=question_data['option4'],
                        correct_option=question_data['correct_option']
                    )
                    db.session.add(question)
                
                db.session.commit()
                print(f"✓ Sample quiz with {len(questions_data)} questions created successfully")

def setup_database():
    """Main function to set up the entire database"""
    print("=== Quiz Master Database Setup ===")
    print()
    
    try:
        create_database()
        create_admin_user()
        create_sample_users()
        create_sample_subjects()
        create_sample_chapters()
        create_sample_quiz()
        
        print()
        print("=== Database Setup Complete! ===")
        print()
        print("🎉 Your Quiz Master database is ready to use!")
        print()
        print("Admin Login:")
        print("  Email: admin@quizmaster.com")
        print("  Password: admin123")
        print()
        print("Sample User Logins:")
        print("  Email: student@example.com")
        print("  Password: student123")
        print()
        print("  Email: john.doe@example.com")
        print("  Password: password123")
        print()
        print("Available Subjects:")
        print("  • Mathematics (with Algebra Basics quiz)")
        print("  • Science")
        print("  • History")
        print("  • English Literature")
        print("  • Computer Science")
        print()
        print("Start your application with: python3 app.py")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        sys.exit(1)

if __name__ == '__main__':
    setup_database()
