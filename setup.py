"""
Setup script for AI Mock Interview System
This script helps initialize the database and verify the installation
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    print("Checking dependencies...")
    try:
        import flask
        import flask_sqlalchemy
        import flask_login
        import werkzeug
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing package: {e.name}")
        print("Please run: pip install -r requirements.txt")
        return False

def setup_database():
    """Initialize the database"""
    print("\nSetting up database...")
    try:
        from app import app, db, Domain
        with app.app_context():
            db.create_all()
            if Domain.query.count() == 0:
                from app import initialize_default_domains
                initialize_default_domains()
            print("✓ Database initialized successfully")
            return True
    except Exception as e:
        print(f"✗ Database setup failed: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 50)
    print("AI Mock Interview System - Setup")
    print("=" * 50)
    
    if not check_dependencies():
        sys.exit(1)
    
    if not setup_database():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nTo run the application:")
    print("  python app.py")
    print("\nThen open your browser to: http://localhost:5000")

if __name__ == '__main__':
    main()

