"""
Analysis routes for LintIQ
Handles file upload and code analysis
"""

from flask import Blueprint, request, jsonify
from src.models.user import User, db
from src.services.analysis_service import AnalysisService
import logging
import zipfile
import io
import os

logger = logging.getLogger(__name__)
analysis_bp = Blueprint('analysis', __name__)
analysis_service = AnalysisService()

def get_current_user():
    """Get current user from JWT token"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    return User.verify_token(token)

@analysis_bp.route('/capabilities', methods=['GET'])
def get_capabilities():
    """Get analysis capabilities and supported languages"""
    try:
        return jsonify({
            'success': True,
            'supported_languages': analysis_service.get_supported_languages(),
            'supported_extensions': ['.py', '.js', '.jsx', '.ts', '.tsx'],
            'max_file_size': '10MB',
            'max_files': 20,
            'features': {
                'static_analysis': True,
                'security_scanning': True,
                'ai_insights': analysis_service.ai_service.is_available(),
                'code_quality': True,
                'performance_analysis': True
            },
            'tools': {
                'python': ['Pylint', 'Bandit'],
                'javascript': ['ESLint'],
                'typescript': ['ESLint'],
                'ai': 'OpenAI GPT-4' if analysis_service.ai_service.is_available() else None
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting capabilities: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get capabilities'
        }), 500

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_code():
    """Analyze uploaded code files"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({
                'success': False,
                'error': 'Authentication required'
            }), 401
        
        # Check if user has credits
        use_ai = request.form.get('use_ai', 'true').lower() == 'true'
        credit_cost = 1 if use_ai else 0  # AI analysis costs 1 credit, basic is free
        
        if credit_cost > 0 and not user.can_analyze(credit_cost):
            return jsonify({
                'success': False,
                'error': f'Insufficient credits. You need {credit_cost} credit(s) but have {user.credits}.',
                'credits_needed': credit_cost,
                'current_credits': user.credits
            }), 402  # Payment Required
        
        # Get uploaded files
        files = request.files.getlist('files')
        if not files:
            return jsonify({
                'success': False,
                'error': 'No files uploaded'
            }), 400
        
        # Process files
        processed_files = []
        total_size = 0
        max_file_size = 10 * 1024 * 1024  # 10MB
        max_total_size = 50 * 1024 * 1024  # 50MB total
        
        for file in files:
            if not file.filename:
                continue
            
            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            if file_size > max_file_size:
                return jsonify({
                    'success': False,
                    'error': f'File {file.filename} is too large (max 10MB)'
                }), 400
            
            total_size += file_size
            if total_size > max_total_size:
                return jsonify({
                    'success': False,
                    'error': 'Total file size exceeds 50MB limit'
                }), 400
            
            # Check if file type is supported
            if not analysis_service.is_supported_file(file.filename):
                continue  # Skip unsupported files
            
            # Read file content
            try:
                content = file.read().decode('utf-8')
            except UnicodeDecodeError:
                continue  # Skip binary files
            
            processed_files.append({
                'name': file.filename,
                'content': content,
                'size': file_size
            })
        
        # Handle ZIP files
        zip_files = [f for f in files if f.filename.endswith('.zip')]
        for zip_file in zip_files:
            try:
                with zipfile.ZipFile(io.BytesIO(zip_file.read())) as zf:
                    for file_info in zf.filelist:
                        if file_info.file_size > max_file_size:
                            continue
                        
                        if analysis_service.is_supported_file(file_info.filename):
                            try:
                                content = zf.read(file_info.filename).decode('utf-8')
                                processed_files.append({
                                    'name': file_info.filename,
                                    'content': content,
                                    'size': file_info.file_size
                                })
                            except (UnicodeDecodeError, zipfile.BadZipFile):
                                continue
            except zipfile.BadZipFile:
                continue
        
        if not processed_files:
            return jsonify({
                'success': False,
                'error': 'No supported code files found'
            }), 400
        
        # Limit number of files
        if len(processed_files) > 20:
            processed_files = processed_files[:20]
        
        # Perform analysis
        analysis_result = analysis_service.analyze_files(processed_files, use_ai)
        
        if analysis_result['success']:
            # Deduct credits if analysis was successful and used AI
            if credit_cost > 0:
                user.use_credits(credit_cost)
                db.session.commit()
                
                # Add credit info to response
                analysis_result['credits_used'] = credit_cost
                analysis_result['remaining_credits'] = user.credits
            
            logger.info(f"Analysis completed for user {user.username}: {len(processed_files)} files")
            
            return jsonify(analysis_result), 200
        else:
            return jsonify(analysis_result), 500
            
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Analysis failed. Please try again.'
        }), 500

@analysis_bp.route('/history', methods=['GET'])
def get_analysis_history():
    """Get analysis history for current user"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({
                'success': False,
                'error': 'Authentication required'
            }), 401
        
        # For now, return basic user analysis info
        # In a real implementation, you'd have a separate analysis history table
        history = []
        
        if user.analyses_count > 0:
            history.append({
                'id': 1,
                'date': user.last_analysis.isoformat() if user.last_analysis else user.created_at.isoformat(),
                'files_count': 1,
                'issues_found': 0,
                'status': 'completed',
                'type': 'code_analysis'
            })
        
        return jsonify({
            'success': True,
            'history': history,
            'total_analyses': user.analyses_count,
            'remaining_credits': user.credits,
            'is_pro': user.is_pro
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting analysis history: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get analysis history'
        }), 500

@analysis_bp.route('/demo', methods=['POST'])
def demo_analysis():
    """Demo analysis with sample code"""
    try:
        # Sample Python code with issues
        sample_code = '''
import os
import subprocess

def process_user_input(user_input):
    # Security issue: SQL injection vulnerability
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    
    # Security issue: Command injection vulnerability
    os.system("echo " + user_input)
    
    # Code quality issue: unused variable
    unused_var = "this is not used"
    
    # Performance issue: inefficient loop
    result = []
    for i in range(1000):
        result.append(str(i))
    
    return query

# Missing docstring and type hints
def calculate(a, b):
    return a + b
'''
        
        files = [{
            'name': 'demo_code.py',
            'content': sample_code,
            'size': len(sample_code)
        }]
        
        # Perform analysis
        analysis_result = analysis_service.analyze_files(files, use_ai=True)
        
        # Add demo info
        analysis_result['is_demo'] = True
        analysis_result['demo_message'] = 'This is a demo analysis with sample code showing various issues'
        
        return jsonify(analysis_result), 200
        
    except Exception as e:
        logger.error(f"Demo analysis error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Demo analysis failed'
        }), 500

