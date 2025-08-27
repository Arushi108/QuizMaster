# Quiz Master - Flask Application

## Overview
This is a comprehensive Quiz Master application built with Flask that allows administrators to create subjects, chapters, and quizzes, while users can register and take quizzes to test their knowledge.

## Features

### Admin Features
- **Dashboard**: Overview of users, subjects, quizzes, and questions
- **Subject Management**: Create, edit, and delete subjects
- **Chapter Management**: Add chapters under subjects
- **Quiz Management**: Create quizzes with specified duration and date
- **Question Management**: Add MCQ questions to quizzes
- **User Management**: View registered users

### User Features
- **Registration & Login**: Secure user authentication
- **Dashboard**: Personal dashboard with available subjects and recent scores
- **Quiz Taking**: Timed quizzes with progress tracking
- **Score Tracking**: View past quiz attempts and performance
- **Performance Analytics**: Visual charts showing progress

## Technology Stack
- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Default Admin Login
- **Email**: admin@quizmaster.com
- **Password**: admin123

## Database Structure
The application uses SQLite with the following main tables:
- **Users**: Store user information and authentication
- **Subjects**: Quiz subjects/categories
- **Chapters**: Sub-topics under subjects
- **Quizzes**: Quiz instances with timing and metadata
- **Questions**: MCQ questions for each quiz
- **Scores**: User quiz attempt results

## File Structure
```
assignment/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── quiz_master.db             # SQLite database (auto-created)
├── templates/
│   ├── base.html              # Base template
│   ├── index.html             # Home page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── admin/
│   │   ├── dashboard.html     # Admin dashboard
│   │   ├── subjects.html      # Subject management
│   │   ├── add_subject.html   # Add subject form
│   │   └── add_question.html  # Add question form
│   └── user/
│       ├── dashboard.html     # User dashboard
│       └── take_quiz.html     # Quiz taking interface
└── README.md                  # This file
```

## Getting Started

1. **First Run**: When you first run the application, an admin user will be automatically created.

2. **Admin Setup**: 
   - Login as admin
   - Create subjects (e.g., Mathematics, Science, History)
   - Add chapters under each subject
   - Create quizzes for chapters
   - Add MCQ questions to quizzes

3. **User Experience**:
   - Register a new user account
   - Browse available subjects and chapters
   - Take quizzes and view results
   - Track performance over time

## Features to Implement (Future Enhancements)
- Search functionality for subjects/quizzes
- Advanced user profile management
- Quiz categories and difficulty levels
- Detailed question analytics
- Export quiz results
- Email notifications
- Mobile responsive design improvements

## Notes
- The database is created automatically on first run
- All quiz timers are enforced on the frontend
- User sessions are managed securely
- The application includes basic validation and error handling
