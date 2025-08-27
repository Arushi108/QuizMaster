from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from models import db
from models.user import User
from models.subject import Subject
from models.chapter import Chapter
from models.quiz import Quiz
from models.question import Question
from models.score import Score

user_bp = Blueprint('user', __name__, url_prefix='/user')

def is_logged_in():
    return 'user_id' in session

def is_admin():
    return session.get('is_admin', False)

def user_required(f):
    """Decorator to check if user is logged in and not admin"""
    def decorated_function(*args, **kwargs):
        if not is_logged_in() or is_admin():
            flash('Access denied', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@user_bp.route('/dashboard')
@user_required
def dashboard():
    # Get available subjects
    subjects = Subject.query.all()
    
    # Get recent quiz attempts
    recent_scores = Score.query.filter_by(user_id=session['user_id']).order_by(Score.time_stamp_of_attempt.desc()).limit(5).all()
    
    return render_template('user/dashboard.html', subjects=subjects, recent_scores=recent_scores)

@user_bp.route('/subject/<int:subject_id>')
@user_required
def subject_chapters(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    
    return render_template('user/subject_chapters.html', subject=subject, chapters=chapters)

@user_bp.route('/chapter/<int:chapter_id>/quizzes')
@user_required
def chapter_quizzes(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    
    return render_template('user/chapter_quizzes.html', chapter=chapter, quizzes=quizzes)

@user_bp.route('/quiz/<int:quiz_id>/start')
@user_required
def start_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    if not questions:
        flash('This quiz has no questions yet.', 'warning')
        return redirect(url_for('user.dashboard'))
    
    # Store quiz start time in session
    session['quiz_start_time'] = datetime.utcnow().isoformat()
    session['quiz_id'] = quiz_id
    
    return render_template('user/take_quiz.html', quiz=quiz, questions=questions)

@user_bp.route('/quiz/<int:quiz_id>/submit', methods=['POST'])
@user_required
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Calculate score
    total_questions = len(questions)
    total_scored = 0
    
    for question in questions:
        user_answer = request.form.get(f'question_{question.id}')
        if user_answer and int(user_answer) == question.correct_option:
            total_scored += 1
    
    # Save score
    score = Score(
        quiz_id=quiz_id,
        user_id=session['user_id'],
        total_scored=total_scored,
        total_questions=total_questions
    )
    db.session.add(score)
    db.session.commit()
    
    # Clear quiz session data
    session.pop('quiz_start_time', None)
    session.pop('quiz_id', None)
    
    flash(f'Quiz completed! You scored {total_scored}/{total_questions}', 'success')
    return redirect(url_for('user.quiz_result', score_id=score.id))

@user_bp.route('/quiz/result/<int:score_id>')
@user_required
def quiz_result(score_id):
    score = Score.query.filter_by(id=score_id, user_id=session['user_id']).first_or_404()
    percentage = round((score.total_scored / score.total_questions) * 100)
    
    return render_template('user/quiz_result.html', score=score, percentage=percentage)

@user_bp.route('/scores')
@user_required
def scores():
    scores = Score.query.filter_by(user_id=session['user_id']).order_by(Score.time_stamp_of_attempt.desc()).all()
    return render_template('user/scores.html', scores=scores)

@user_bp.route('/profile')
@user_required
def profile():
    user = User.query.get_or_404(session['user_id'])
    return render_template('user/profile.html', user=user)

@user_bp.route('/profile/edit', methods=['GET', 'POST'])
@user_required
def edit_profile():
    user = User.query.get_or_404(session['user_id'])
    
    if request.method == 'POST':
        user.full_name = request.form['full_name']
        user.qualification = request.form.get('qualification', '')
        
        # Handle date of birth
        dob_str = request.form.get('dob')
        if dob_str:
            try:
                user.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format', 'error')
                return render_template('user/edit_profile.html', user=user)
        
        db.session.commit()
        
        # Update session data
        session['full_name'] = user.full_name
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user.profile'))
    
    return render_template('user/edit_profile.html', user=user)

@user_bp.route('/profile/change-password', methods=['GET', 'POST'])
@user_required
def change_password():
    user = User.query.get_or_404(session['user_id'])
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Verify current password
        import hashlib
        if user.password_hash != hashlib.md5(current_password.encode()).hexdigest():
            flash('Current password is incorrect', 'error')
            return render_template('user/change_password.html')
        
        # Validate new password
        if len(new_password) < 6:
            flash('New password must be at least 6 characters long', 'error')
            return render_template('user/change_password.html')
        
        # Check if new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return render_template('user/change_password.html')
        
        # Update password
        user.password_hash = hashlib.md5(new_password.encode()).hexdigest()
        db.session.commit()
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('user.profile'))
    
    return render_template('user/change_password.html')
