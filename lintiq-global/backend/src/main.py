"""
LintIQ - AI-Powered Code Analysis Platform
Main Flask application with DPO Group payment integration
"""

import os
import logging
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.auth import auth_bp
from src.routes.payments import payments_bp
from src.routes.analysis import analysis_bp
from src.routes.user import user_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure Flask application"""
    
    app = Flask(__name__, static_folder='static')
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database/app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
    
    # Enable CORS for all routes
    CORS(app, origins="*")
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(payments_bp, url_prefix='/api/payments')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'service': 'LintIQ API',
            'version': '1.0.0',
            'features': {
                'authentication': True,
                'code_analysis': True,
                'ai_insights': bool(os.getenv('OPENAI_API_KEY')),
                'payments': bool(os.getenv('DPO_COMPANY_TOKEN')),
                'database': True
            }
        })
    
    # API info endpoint
    @app.route('/api')
    def api_info():
        """API information endpoint"""
        return jsonify({
            'service': 'LintIQ API',
            'version': '1.0.0',
            'description': 'AI-powered code analysis platform for Botswana',
            'endpoints': {
                'authentication': '/api/auth',
                'payments': '/api/payments',
                'analysis': '/api/analysis',
                'user': '/api/user'
            },
            'payment_gateway': 'DPO Group',
            'supported_languages': ['Python', 'JavaScript', 'TypeScript'],
            'documentation': 'https://github.com/yourusername/lintiq'
        })
    
    # Serve React frontend
    @app.route('/')
    def serve_frontend():
        """Serve React frontend"""
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static_files(path):
        """Serve static files or fallback to index.html for React routing"""
        try:
            return send_from_directory(app.static_folder, path)
        except:
            # Fallback to index.html for React Router
            return send_from_directory(app.static_folder, 'index.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'success': False,
            'error': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    
    @app.errorhandler(413)
    def file_too_large(error):
        """Handle file too large errors"""
        return jsonify({
            'success': False,
            'error': 'File too large. Maximum size is 50MB.'
        }), 413
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    # Development server
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Starting LintIQ server on port {port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"OpenAI API configured: {bool(os.getenv('OPENAI_API_KEY'))}")
    logger.info(f"DPO payment configured: {bool(os.getenv('DPO_COMPANY_TOKEN'))}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )

