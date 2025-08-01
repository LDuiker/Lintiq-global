"""
User model for LintIQ application
Simple user management with credits and authentication
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
import os

db = SQLAlchemy()

class User(db.Model):
    """User model with authentication and credit management"""
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Credit system
    credits = db.Column(db.Integer, default=10)  # Free tier gets 10 credits
    total_spent = db.Column(db.Integer, default=0)  # Total money spent in cents
    
    # Account info
    is_pro = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Usage tracking
    analyses_count = db.Column(db.Integer, default=0)
    last_analysis = db.Column(db.DateTime)
    
    def __init__(self, username, email, password, credits=10):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.credits = credits
        self.created_at = datetime.utcnow()
    
    def check_password(self, password):
        """Check if provided password matches user's password"""
        return check_password_hash(self.password_hash, password)
    
    def generate_token(self):
        """Generate JWT token for user authentication"""
        payload = {
            'user_id': self.id,
            'username': self.username,
            'email': self.email,
            'exp': datetime.utcnow() + timedelta(days=7)  # Token expires in 7 days
        }
        
        secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
        return jwt.encode(payload, secret_key, algorithm='HS256')
    
    @staticmethod
    def verify_token(token):
        """Verify JWT token and return user"""
        try:
            secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            user = User.query.get(payload['user_id'])
            return user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, KeyError):
            return None
    
    def can_analyze(self, cost=1):
        """Check if user has enough credits for analysis"""
        return self.credits >= cost
    
    def use_credits(self, amount=1):
        """Deduct credits from user account"""
        if self.can_analyze(amount):
            self.credits -= amount
            self.analyses_count += 1
            self.last_analysis = datetime.utcnow()
            return True
        return False
    
    def add_credits(self, amount):
        """Add credits to user account"""
        self.credits += amount
    
    def to_dict(self):
        """Convert user to dictionary for JSON response"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'credits': self.credits,
            'is_pro': self.is_pro,
            'total_spent': self.total_spent,
            'analyses_count': self.analyses_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'last_analysis': self.last_analysis.isoformat() if self.last_analysis else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

