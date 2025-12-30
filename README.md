# AI-Driven Mock Interview System

A comprehensive web-based application that helps students and job seekers practice interviews using AI-generated questions, automated evaluation, and performance feedback.

## Features

### Core Functionality

- **User Authentication**: Secure registration and login with password hashing
- **Domain Selection**: Choose from multiple interview domains (IT, HR, Finance, Management)
- **AI Question Generator**: Dynamic question generation based on selected domain
- **Interview Simulation**: Real-time interview environment with one-by-one question display
- **Automated Evaluation**: Rule-based scoring system evaluating:
  - Clarity of response
  - Accuracy and relevance
  - Communication quality
  - Confidence level
- **Performance Reports**: Detailed feedback with strengths and improvement suggestions
- **Database Management**: Secure storage of user data, interview history, and analytics

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (can be configured for MySQL)
- **AI/NLP**: Rule-based question generation and evaluation
- **Security**: Werkzeug password hashing, Flask-Login session management

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd A:\aimock
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/macOS:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`

## Project Structure

```
aimock/
├── app.py                 # Main Flask application
├── question_generator.py  # AI question generation module
├── evaluator.py          # Answer evaluation module
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── domains.html
│   ├── interview.html
│   └── results.html
└── static/               # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Usage Guide

### For Users

1. **Registration**
   - Click "Register" on the homepage
   - Fill in username, email, and password
   - Optionally provide your full name

2. **Starting an Interview**
   - Login to your account
   - Navigate to "Start Interview" from the dashboard
   - Select your desired domain (IT, HR, Finance, Management)
   - Wait for questions to be generated

3. **Taking the Interview**
   - Read each question carefully
   - Type your answer in the text area
   - Click "Submit Answer" to get instant evaluation
   - Review your scores and feedback
   - Click "Next Question" to continue
   - Complete all questions and finish the interview

4. **Viewing Results**
   - After completing an interview, view detailed results
   - Check your overall score and per-question breakdown
   - Review strengths and areas for improvement
   - Use feedback to improve future performance

### For Developers

#### Database Models

- **User**: Stores user credentials and authentication data
- **UserProfile**: Extended user information and statistics
- **Domain**: Interview domain categories and question templates
- **Interview**: Interview session records
- **Question**: Individual interview questions
- **Answer**: User answers with evaluation scores

#### Key Modules

- **question_generator.py**: Generates domain-specific questions using templates and knowledge bases
- **evaluator.py**: Evaluates answers using rule-based scoring on multiple criteria

#### Customization

- **Add New Domains**: Modify `initialize_default_domains()` in `app.py`
- **Adjust Question Generation**: Edit `question_generator.py` knowledge bases
- **Modify Evaluation Criteria**: Update scoring logic in `evaluator.py`
- **Change Database**: Update `SQLALCHEMY_DATABASE_URI` in `app.py`

## Configuration

### Environment Variables

You can configure the application using environment variables:

- `SECRET_KEY`: Flask secret key for session management (default: development key)
- `DATABASE_URL`: Database connection string (default: SQLite)

Example:
```bash
export SECRET_KEY='your-secret-key-here'
export DATABASE_URL='mysql://user:password@localhost/interview_db'
```

## Security Features

- Password hashing using Werkzeug's secure password hashing
- Session management with Flask-Login
- SQL injection protection via SQLAlchemy ORM
- User authentication required for protected routes

## Future Enhancements

Potential improvements for the system:

- Voice input support for answers
- Advanced NLP-based question generation
- Machine learning-based answer evaluation
- Multi-language support
- Interview scheduling and reminders
- Video interview simulation
- Integration with job boards
- Advanced analytics and progress tracking

## Troubleshooting

### Common Issues

1. **Database errors**: Ensure SQLite is accessible or configure MySQL connection
2. **Import errors**: Verify all dependencies are installed via `pip install -r requirements.txt`
3. **Port already in use**: Change the port in `app.py` (last line) or stop the conflicting service

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions, please refer to the project documentation or create an issue in the project repository.

