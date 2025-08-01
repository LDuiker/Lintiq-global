"""
Authentication routes for LintIQ
Handles user registration, login, and demo access
"""

from flask import Blueprint, request, jsonify
from src.models.user import User, db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not username or not email or not password:
            return jsonify({
                'success': False,
                'error': 'Username, email, and password are required'
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'success': False,
                'error': 'Password must be at least 6 characters long'
            }), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'error': 'Username already exists'
            }), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False,
                'error': 'Email already registered'
            }), 400
        
        # Create new user
        user = User(username=username, email=email, password=password, credits=10)
        db.session.add(user)
        db.session.commit()
        
        # Generate token
        token = user.generate_token()
        
        logger.info(f"New user registered: {username}")
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user': user.to_dict(),
            'token': token
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Registration failed. Please try again.'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        # Validate input
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'error': 'Username and password are required'
            }), 400
        
        # Find user (allow login with username or email)
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user or not user.check_password(password):
            return jsonify({
                'success': False,
                'error': 'Invalid username or password'
            }), 401
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Generate token
        token = user.generate_token()
        
        logger.info(f"User logged in: {user.username}")
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user.to_dict(),
            'token': token
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Login failed. Please try again.'
        }), 500

@auth_bp.route('/demo', methods=['POST'])
def demo_login():
    """Create or login to demo account"""
    try:
        # Check if demo user exists
        demo_user = User.query.filter_by(username='demo_user').first()
        
        if not demo_user:
            # Create demo user
            demo_user = User(
                username='demo_user',
                email='demo@lintiq.com',
                password='demo123',
                credits=100  # Demo gets more credits
            )
            demo_user.is_pro = True  # Demo has pro features
            db.session.add(demo_user)
            db.session.commit()
            logger.info("Demo user created")
        else:
            # Reset demo user credits if low
            if demo_user.credits < 10:
                demo_user.credits = 100
                db.session.commit()
                logger.info("Demo user credits reset")
        
        # Update last login
        demo_user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Generate token
        token = demo_user.generate_token()
        
        return jsonify({
            'success': True,
            'message': 'Demo access granted',
            'user': demo_user.to_dict(),
            'token': token
        }), 200
        
    except Exception as e:
        logger.error(f"Demo login error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Demo access failed. Please try again.'
        }), 500

@auth_bp.route('/verify', methods=['POST'])
def verify_token():
    """Verify JWT token"""
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'No valid authorization header'
            }), 401
        
        token = auth_header.split(' ')[1]
        user = User.verify_token(token)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired token'
            }), 401
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Token verification failed'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user (client-side token removal)"""
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    }), 200

