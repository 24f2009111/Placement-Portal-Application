#!/usr/bin/env python
"""
Placement Portal Application - Setup and Initialization Script
Run this script once to initialize the database and create the admin account.
"""

import sys
import os
from werkzeug.security import generate_password_hash

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db
from models import User

def init_database():
    """Initialize the database and create default admin user."""
    with app.app_context():
        print("Initializing database...")
        db.create_all()
        print("✓ Database tables created successfully")
        
        # Check if admin exists
        admin_user = User.query.filter_by(role='admin').first()
        if not admin_user:
            print("\nCreating default admin account...")
            admin = User(
                username='admin',
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin account created")
            print("\n" + "="*50)
            print("DEFAULT ADMIN CREDENTIALS:")
            print("="*50)
            print("Username: admin")
            print("Password: admin123")
            print("="*50)
            print("\n⚠️  Please change the admin password in production!")
        else:
            print("✓ Admin account already exists")
        
        print("\n✅ Database initialization complete!")
        print("\nYou can now run the application with:")
        print("  python app.py")
        print("\nThen open: http://localhost:5000")

if __name__ == '__main__':
    init_database()