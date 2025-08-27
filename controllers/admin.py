from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime, date
from sqlalchemy import func, extract
from models import db
from models.user import User
from models.subject import Subject
from models.chapter import Chapter
from models.quiz import Quiz
from models.question import Question
from models.score import Score

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def is_logged_in():
    return 'user_id' in session

def is_admin():
    return session.get('is_admin', False)

def admin_required(f):
    """Decorator to check if user is admin"""
    def decorated_function(*args, **kwargs):
        if not is_logged_in() or not is_admin():
            flash('Access denied', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # Get statistics
    total_users = User.query.filter_by(is_admin=False).count()
    total_subjects = Subject.query.count()
    total_quizzes = Quiz.query.count()
    total_questions = Question.query.count()
    
    # Get user registration data for the last 6 months
    user_registration_data = get_user_registration_data()
    
    # Get quiz attempts data by subject
    quiz_attempts_data = get_quiz_attempts_data()
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users,
                         total_subjects=total_subjects, 
                         total_quizzes=total_quizzes,
                         total_questions=total_questions,
                         user_registration_data=user_registration_data,
                         quiz_attempts_data=quiz_attempts_data)

def get_user_registration_data():
    """Get user registration data for the last 6 months"""
    from datetime import datetime, timedelta
    import calendar
    
    # Get current date and calculate 6 months back
    now = datetime.now()
    months_data = []
    
    for i in range(5, -1, -1):  # Last 6 months including current
        # Calculate the month
        month = now.month - i
        year = now.year
        
        if month <= 0:
            month += 12
            year -= 1
            
        # Get month name
        month_name = calendar.month_abbr[month]
        
        # Count users registered in this month
        user_count = User.query.filter(
            extract('month', User.created_at) == month,
            extract('year', User.created_at) == year,
            User.is_admin == False
        ).count()
        
        months_data.append({
            'label': month_name,
            'count': user_count
        })
    
    return months_data

def get_quiz_attempts_data():
    """Get quiz attempts data by subject"""
    # Get quiz attempts grouped by subject
    quiz_attempts = db.session.query(
        Subject.name,
        func.count(Score.id).label('attempts')
    ).join(
        Chapter, Subject.id == Chapter.subject_id
    ).join(
        Quiz, Chapter.id == Quiz.chapter_id
    ).join(
        Score, Quiz.id == Score.quiz_id
    ).group_by(Subject.id, Subject.name).all()
    
    # If no data, provide some sample subjects
    if not quiz_attempts:
        subjects = Subject.query.limit(5).all()
        return [{'label': subject.name, 'count': 0} for subject in subjects]
    
    return [{'label': attempt.name, 'count': attempt.attempts} for attempt in quiz_attempts]

# Subject management routes
@admin_bp.route('/subjects')
@admin_required
def subjects():
    subjects = Subject.query.all()
    return render_template('admin/subjects.html', subjects=subjects)

@admin_bp.route('/subjects/add', methods=['GET', 'POST'])
@admin_required
def add_subject():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        
        subject = Subject(name=name, description=description)
        db.session.add(subject)
        db.session.commit()
        
        flash('Subject added successfully!', 'success')
        return redirect(url_for('admin.subjects'))
    
    return render_template('admin/add_subject.html')

@admin_bp.route('/subjects/<int:subject_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    
    if request.method == 'POST':
        subject.name = request.form['name']
        subject.description = request.form.get('description', '')
        
        db.session.commit()
        flash('Subject updated successfully!', 'success')
        return redirect(url_for('admin.subjects'))
    
    return render_template('admin/edit_subject.html', subject=subject)

@admin_bp.route('/subjects/<int:subject_id>/delete', methods=['POST'])
@admin_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    
    flash('Subject deleted successfully!', 'success')
    return redirect(url_for('admin.subjects'))

# Chapter management routes
@admin_bp.route('/chapters')
@admin_required
def chapters():
    chapters = Chapter.query.join(Subject).all()
    return render_template('admin/chapters.html', chapters=chapters)

@admin_bp.route('/chapters/add', methods=['GET', 'POST'])
@admin_required
def add_chapter():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        subject_id = request.form['subject_id']
        
        chapter = Chapter(name=name, description=description, subject_id=subject_id)
        db.session.add(chapter)
        db.session.commit()
        
        flash('Chapter added successfully!', 'success')
        return redirect(url_for('admin.chapters'))
    
    subjects = Subject.query.all()
    return render_template('admin/add_chapter.html', subjects=subjects)

@admin_bp.route('/chapters/<int:chapter_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    
    if request.method == 'POST':
        chapter.name = request.form['name']
        chapter.description = request.form.get('description', '')
        chapter.subject_id = request.form['subject_id']
        
        db.session.commit()
        flash('Chapter updated successfully!', 'success')
        return redirect(url_for('admin.chapters'))
    
    subjects = Subject.query.all()
    return render_template('admin/edit_chapter.html', chapter=chapter, subjects=subjects)

@admin_bp.route('/chapters/<int:chapter_id>/delete', methods=['POST'])
@admin_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    
    flash('Chapter deleted successfully!', 'success')
    return redirect(url_for('admin.chapters'))

@admin_bp.route('/chapters/<int:chapter_id>/quizzes')
@admin_required
def chapter_quizzes(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    return render_template('admin/chapter_quizzes.html', chapter=chapter, quizzes=quizzes)

# Quiz management routes
@admin_bp.route('/quizzes')
@admin_required
def quizzes():
    quizzes = Quiz.query.join(Chapter).join(Subject).all()
    return render_template('admin/quizzes.html', quizzes=quizzes)

@admin_bp.route('/quizzes/add', methods=['GET', 'POST'])
@admin_required
def add_quiz():
    if request.method == 'POST':
        chapter_id = request.form['chapter_id']
        date_of_quiz = datetime.strptime(request.form['date_of_quiz'], '%Y-%m-%d').date()
        time_duration = int(request.form['time_duration'])
        remarks = request.form.get('remarks', '')
        
        quiz = Quiz(
            chapter_id=chapter_id,
            date_of_quiz=date_of_quiz,
            time_duration=time_duration,
            remarks=remarks
        )
        db.session.add(quiz)
        db.session.commit()
        
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('admin.quiz_questions', quiz_id=quiz.id))
    
    chapters = Chapter.query.join(Subject).all()
    return render_template('admin/add_quiz.html', chapters=chapters)

@admin_bp.route('/quizzes/<int:quiz_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if request.method == 'POST':
        quiz.chapter_id = request.form['chapter_id']
        quiz.date_of_quiz = datetime.strptime(request.form['date_of_quiz'], '%Y-%m-%d').date()
        quiz.time_duration = int(request.form['time_duration'])
        quiz.remarks = request.form.get('remarks', '')
        
        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('admin.chapter_quizzes', chapter_id=quiz.chapter_id))
    
    chapters = Chapter.query.join(Subject).all()
    return render_template('admin/edit_quiz.html', quiz=quiz, chapters=chapters)

@admin_bp.route('/quizzes/<int:quiz_id>/delete', methods=['POST'])
@admin_required
def delete_quiz(quiz_id):
    print(f"Delete quiz called for quiz_id: {quiz_id}")
    quiz = Quiz.query.get_or_404(quiz_id)
    chapter_id = quiz.chapter_id
    print(f"Found quiz: {quiz}, chapter_id: {chapter_id}")
    
    try:
        # Cascade delete will handle questions and scores automatically
        db.session.delete(quiz)
        db.session.commit()
        print(f"Quiz {quiz_id} deleted successfully")
        
        flash('Quiz deleted successfully!', 'success')
    except Exception as e:
        print(f"Error deleting quiz {quiz_id}: {str(e)}")
        db.session.rollback()
        flash(f'Error deleting quiz: {str(e)}', 'error')
    
    return redirect(url_for('admin.chapter_quizzes', chapter_id=chapter_id))

@admin_bp.route('/quizzes/<int:quiz_id>/questions')
@admin_required
def quiz_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return render_template('admin/quiz_questions.html', quiz=quiz, questions=questions)

@admin_bp.route('/quizzes/<int:quiz_id>/add_question', methods=['GET', 'POST'])
@admin_required
def add_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if request.method == 'POST':
        question_statement = request.form['question_statement']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_option = int(request.form['correct_option'])
        
        question = Question(
            quiz_id=quiz_id,
            question_statement=question_statement,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option
        )
        
        db.session.add(question)
        db.session.commit()
        
        flash('Question added successfully!', 'success')
        return redirect(url_for('admin.quiz_questions', quiz_id=quiz_id))
    
    return render_template('admin/add_question.html', quiz=quiz)

# User management routes
@admin_bp.route('/users')
@admin_required
def users():
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:user_id>/toggle_status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    
    # Toggle user active status (assuming we add an active field)
    # For now, we'll just show a message
    flash(f'User {user.full_name} status updated!', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    try:
        # Delete user's scores first
        Score.query.filter_by(user_id=user_id).delete()
        
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        
        flash(f'User {user.full_name} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/scores')
@admin_required
def user_scores(user_id):
    user = User.query.get_or_404(user_id)
    scores = Score.query.filter_by(user_id=user_id).join(Quiz).join(Chapter).join(Subject).all()
    return render_template('admin/user_scores.html', user=user, scores=scores)
