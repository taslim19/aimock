# Quick Start Guide

## Installation (5 minutes)

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run setup script (optional but recommended)**
   ```bash
   python setup.py
   ```
   This will verify dependencies and initialize the database.

3. **Start the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to: `http://localhost:5000`

## First Steps

1. **Register a new account**
   - Click "Register" on the homepage
   - Fill in your details
   - You'll be automatically logged in

2. **Start your first interview**
   - From the dashboard, click "Start New Interview"
   - Choose a domain (IT, HR, Finance, or Management)
   - Wait for questions to load

3. **Answer questions**
   - Read each question carefully
   - Type your answer in the text area
   - Click "Submit Answer" to get instant feedback
   - Review your scores and continue to the next question

4. **View results**
   - After completing all questions, click "Complete Interview"
   - Review your detailed performance report
   - Check strengths and areas for improvement

## Features Overview

- **Multiple Domains**: IT/Software Engineering, HR, Finance, Management
- **AI-Generated Questions**: Dynamic questions tailored to your selected domain
- **Instant Evaluation**: Get feedback immediately after each answer
- **Performance Tracking**: View your interview history and statistics
- **Detailed Reports**: Comprehensive feedback with actionable insights

## Troubleshooting

**Port 5000 already in use?**
- Edit `app.py` and change the port in the last line:
  ```python
  app.run(debug=True, host='0.0.0.0', port=8080)  # Use port 8080 instead
  ```

**Database errors?**
- Delete `interview_system.db` and run `python setup.py` again
- Or manually run: `python app.py` (database will be created automatically)

**Import errors?**
- Make sure you've activated your virtual environment
- Run: `pip install -r requirements.txt`

## Next Steps

- Practice interviews in different domains
- Review your performance trends in the dashboard
- Use feedback to improve your answers
- Try answering questions more comprehensively for better scores

