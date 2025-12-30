"""
AI-Driven Mock Interview System
Main Flask Application
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import os
import json
import random
import re
from question_generator import QuestionGenerator
from evaluator import AnswerEvaluator

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///interview_system.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Custom Jinja2 filter for JSON parsing
@app.template_filter('from_json')
def from_json_filter(value):
    """Parse JSON string to Python object"""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return []
    return value if isinstance(value, list) else []

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize AI components
question_generator = QuestionGenerator()
evaluator = AnswerEvaluator()


# Database Models
class User(UserMixin, db.Model):
    """User model for authentication and profiles"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    interviews = db.relationship('Interview', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserProfile(db.Model):
    """Extended user profile information"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100))
    experience_level = db.Column(db.String(50))  # Beginner, Intermediate, Advanced
    preferred_domains = db.Column(db.Text)  # JSON array of domains
    total_interviews = db.Column(db.Integer, default=0)
    average_score = db.Column(db.Float, default=0.0)


class Domain(db.Model):
    """Interview domain categories"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    question_templates = db.Column(db.Text)  # JSON array of question templates
    difficulty_levels = db.Column(db.Text)  # JSON array of difficulty levels


class Interview(db.Model):
    """Interview session records"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    started_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed
    overall_score = db.Column(db.Float)
    questions = db.relationship('Question', backref='interview', lazy=True, cascade='all, delete-orphan')


class Question(db.Model):
    """Interview questions"""
    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interview.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50))  # technical, behavioral, situational
    difficulty = db.Column(db.String(20))  # easy, medium, hard
    order_number = db.Column(db.Integer)
    answer = db.relationship('Answer', backref='question', uselist=False, cascade='all, delete-orphan')


class Answer(db.Model):
    """User answers to interview questions"""
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    clarity_score = db.Column(db.Float)
    accuracy_score = db.Column(db.Float)
    communication_score = db.Column(db.Float)
    confidence_score = db.Column(db.Float)
    overall_score = db.Column(db.Float)
    feedback = db.Column(db.Text)
    strengths = db.Column(db.Text)  # JSON array
    improvements = db.Column(db.Text)  # JSON array
    submitted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Routes
@app.route('/')
def index():
    """Home page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name', '')

        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already exists'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already registered'}), 400

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Create user profile
        profile = UserProfile(user_id=user.id, full_name=full_name)
        db.session.add(profile)
        db.session.commit()

        login_user(user)
        return jsonify({'success': True, 'message': 'Registration successful', 'redirect': url_for('dashboard')})

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return jsonify({'success': True, 'message': 'Login successful', 'redirect': url_for('dashboard')})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user_interviews = Interview.query.filter_by(user_id=current_user.id).order_by(Interview.started_at.desc()).limit(10).all()
    
    # Calculate statistics
    total_interviews = Interview.query.filter_by(user_id=current_user.id).count()
    completed_interviews = Interview.query.filter_by(user_id=current_user.id, status='completed').count()
    
    avg_score = db.session.query(db.func.avg(Interview.overall_score)).filter_by(
        user_id=current_user.id, status='completed'
    ).scalar() or 0.0

    return render_template('dashboard.html', 
                         interviews=user_interviews,
                         total_interviews=total_interviews,
                         completed_interviews=completed_interviews,
                         avg_score=round(avg_score, 2))


@app.route('/domains')
@login_required
def domains():
    """Domain selection page"""
    available_domains = Domain.query.all()
    if not available_domains:
        # Initialize default domains if none exist
        initialize_default_domains()
        available_domains = Domain.query.all()
    
    return render_template('domains.html', domains=available_domains)


@app.route('/start-interview', methods=['POST'])
@login_required
def start_interview():
    """Start a new interview session"""
    data = request.get_json()
    domain_name = data.get('domain')

    # Create new interview
    interview = Interview(user_id=current_user.id, domain=domain_name)
    db.session.add(interview)
    db.session.commit()

    # Generate questions for this interview
    questions = question_generator.generate_questions(domain_name, num_questions=5)
    
    for idx, q_data in enumerate(questions):
        question = Question(
            interview_id=interview.id,
            question_text=q_data['text'],
            question_type=q_data.get('type', 'technical'),
            difficulty=q_data.get('difficulty', 'medium'),
            order_number=idx + 1
        )
        db.session.add(question)
    
    db.session.commit()

    return jsonify({
        'success': True,
        'interview_id': interview.id,
        'redirect': url_for('interview', interview_id=interview.id)
    })


@app.route('/interview/<int:interview_id>')
@login_required
def interview(interview_id):
    """Interview session page"""
    interview_obj = Interview.query.get_or_404(interview_id)
    
    if interview_obj.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))

    questions = Question.query.filter_by(interview_id=interview_id).order_by(Question.order_number).all()
    # Convert SQLAlchemy objects to dictionaries for JSON serialization
    questions_data = [{
        'id': q.id,
        'question_text': q.question_text,
        'question_type': q.question_type,
        'difficulty': q.difficulty,
        'order_number': q.order_number
    } for q in questions]
    return render_template('interview.html', interview=interview_obj, questions=questions_data)


@app.route('/submit-answer', methods=['POST'])
@login_required
def submit_answer():
    """Submit and evaluate an answer"""
    data = request.get_json()
    question_id = data.get('question_id')
    answer_text = data.get('answer_text')

    question = Question.query.get_or_404(question_id)
    
    if question.interview.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    # Evaluate the answer
    evaluation = evaluator.evaluate_answer(answer_text, question.question_text, question.difficulty)

    # Store the answer
    answer = Answer(
        question_id=question_id,
        answer_text=answer_text,
        clarity_score=evaluation['clarity'],
        accuracy_score=evaluation['accuracy'],
        communication_score=evaluation['communication'],
        confidence_score=evaluation['confidence'],
        overall_score=evaluation['overall'],
        feedback=evaluation['feedback'],
        strengths=json.dumps(evaluation['strengths']),
        improvements=json.dumps(evaluation['improvements'])
    )
    db.session.add(answer)
    db.session.commit()

    return jsonify({
        'success': True,
        'evaluation': evaluation
    })


@app.route('/complete-interview/<int:interview_id>', methods=['POST'])
@login_required
def complete_interview(interview_id):
    """Complete an interview and generate final report"""
    interview_obj = Interview.query.get_or_404(interview_id)
    
    if interview_obj.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    # Calculate overall score
    answers = db.session.query(Answer).join(Question).filter(
        Question.interview_id == interview_id
    ).all()

    if answers:
        overall_score = sum([ans.overall_score for ans in answers]) / len(answers)
        interview_obj.overall_score = overall_score
    
    interview_obj.status = 'completed'
    interview_obj.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    # Update user profile statistics
    if current_user.profile:
        current_user.profile.total_interviews = Interview.query.filter_by(
            user_id=current_user.id, status='completed'
        ).count()
        avg_score = db.session.query(db.func.avg(Interview.overall_score)).filter_by(
            user_id=current_user.id, status='completed'
        ).scalar() or 0.0
        current_user.profile.average_score = avg_score
        db.session.commit()

    return jsonify({
        'success': True,
        'redirect': url_for('results', interview_id=interview_id)
    })


@app.route('/results/<int:interview_id>')
@login_required
def results(interview_id):
    """Interview results and feedback page"""
    interview_obj = Interview.query.get_or_404(interview_id)
    
    if interview_obj.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))

    questions = Question.query.filter_by(interview_id=interview_id).order_by(Question.order_number).all()
    answers_data = []
    
    for question in questions:
        answer = Answer.query.filter_by(question_id=question.id).first()
        answers_data.append({
            'question': question,
            'answer': answer
        })

    return render_template('results.html', interview=interview_obj, answers_data=answers_data)


def initialize_default_domains():
    """Initialize default interview domains"""
    domains_data = [
        {
            'name': 'IT/Software Engineering',
            'description': 'Technical interviews for software development roles',
            'question_templates': [
                'Explain {topic} in detail',
                'What is the difference between {concept1} and {concept2}?',
                'How would you implement {feature}?',
                'Describe your experience with {technology}',
                'What are the best practices for {topic}?'
            ],
            'difficulty_levels': ['easy', 'medium', 'hard']
        },
        {
            'name': 'HR/Human Resources',
            'description': 'Behavioral and situational HR interview questions',
            'question_templates': [
                'Tell me about yourself',
                'Describe a time when you {situation}',
                'How do you handle {challenge}?',
                'What are your strengths and weaknesses?',
                'Why do you want to work here?'
            ],
            'difficulty_levels': ['easy', 'medium']
        },
        {
            'name': 'Finance',
            'description': 'Financial analysis and accounting interview questions',
            'question_templates': [
                'Explain {financial_concept}',
                'How would you analyze {scenario}?',
                'What is the impact of {event} on financial markets?',
                'Describe your experience with {financial_tool}',
                'How do you evaluate {investment_type}?'
            ],
            'difficulty_levels': ['medium', 'hard']
        },
        {
            'name': 'Management',
            'description': 'Leadership and management interview questions',
            'question_templates': [
                'How do you motivate your team?',
                'Describe a time you had to make a difficult decision',
                'How do you handle conflict in the workplace?',
                'What is your leadership style?',
                'How do you prioritize tasks and manage time?'
            ],
            'difficulty_levels': ['medium', 'hard']
        }
    ]

    for domain_data in domains_data:
        domain = Domain(
            name=domain_data['name'],
            description=domain_data['description'],
            question_templates=json.dumps(domain_data['question_templates']),
            difficulty_levels=json.dumps(domain_data['difficulty_levels'])
        )
        db.session.add(domain)
    
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if Domain.query.count() == 0:
            initialize_default_domains()
    app.run(debug=True, host='0.0.0.0', port=5000)

