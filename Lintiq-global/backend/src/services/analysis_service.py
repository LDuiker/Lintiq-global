"""
Code Analysis Service for LintIQ
Handles file processing and analysis orchestration
"""

import os
import tempfile
import subprocess
import json
import logging
from typing import Dict, List, Any, Optional
from .ai_service import AIService

logger = logging.getLogger(__name__)

class AnalysisService:
    """Orchestrates code analysis using multiple tools"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.supported_extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript'
        }
    
    def analyze_files(self, files: List[Dict[str, Any]], use_ai: bool = True) -> Dict[str, Any]:
        """
        Analyze multiple code files
        
        Args:
            files: List of file dictionaries with 'name', 'content', 'size'
            use_ai: Whether to include AI analysis
            
        Returns:
            Complete analysis results
        """
        try:
            results = {
                'success': True,
                'files_analyzed': len(files),
                'total_issues': 0,
                'analysis_results': [],
                'summary': {
                    'critical_issues': 0,
                    'high_issues': 0,
                    'medium_issues': 0,
                    'low_issues': 0,
                    'overall_score': 0
                },
                'ai_analysis': None
            }
            
            total_score = 0
            analyzed_files = 0
            
            # Analyze each file
            for file_info in files:
                file_result = self._analyze_single_file(
                    file_info['name'],
                    file_info['content'],
                    use_ai
                )
                
                if file_result['success']:
                    results['analysis_results'].append(file_result)
                    results['total_issues'] += len(file_result.get('issues', []))
                    
                    # Count issues by severity
                    for issue in file_result.get('issues', []):
                        severity = issue.get('severity', 'low').lower()
                        if severity == 'critical':
                            results['summary']['critical_issues'] += 1
                        elif severity == 'high':
                            results['summary']['high_issues'] += 1
                        elif severity == 'medium':
                            results['summary']['medium_issues'] += 1
                        else:
                            results['summary']['low_issues'] += 1
                    
                    # Add to overall score calculation
                    if 'score' in file_result:
                        total_score += file_result['score']
                        analyzed_files += 1
            
            # Calculate overall score
            if analyzed_files > 0:
                results['summary']['overall_score'] = round(total_score / analyzed_files, 1)
            
            # Add AI analysis for the entire codebase if requested
            if use_ai and self.ai_service.is_available() and files:
                combined_code = self._combine_files_for_ai(files)
                ai_result = self.ai_service.analyze_code(
                    combined_code,
                    'mixed',
                    f"{len(files)} files"
                )
                if ai_result['success']:
                    results['ai_analysis'] = ai_result['analysis']
            
            return results
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'files_analyzed': 0,
                'analysis_results': []
            }
    
    def _analyze_single_file(self, filename: str, content: str, use_ai: bool) -> Dict[str, Any]:
        """Analyze a single code file"""
        
        try:
            # Determine file language
            file_ext = os.path.splitext(filename)[1].lower()
            language = self.supported_extensions.get(file_ext, 'unknown')
            
            if language == 'unknown':
                return {
                    'success': False,
                    'filename': filename,
                    'error': f'Unsupported file type: {file_ext}'
                }
            
            result = {
                'success': True,
                'filename': filename,
                'language': language,
                'file_size': len(content),
                'issues': [],
                'metrics': {},
                'score': 8  # Default good score
            }
            
            # Run static analysis based on language
            if language == 'python':
                static_result = self._analyze_python(content, filename)
            elif language in ['javascript', 'typescript']:
                static_result = self._analyze_javascript(content, filename)
            else:
                static_result = {'issues': [], 'metrics': {}}
            
            result['issues'].extend(static_result.get('issues', []))
            result['metrics'].update(static_result.get('metrics', {}))
            
            # Add AI analysis if requested and available
            if use_ai and self.ai_service.is_available():
                ai_result = self.ai_service.analyze_code(content, language, filename)
                if ai_result['success']:
                    result['ai_analysis'] = ai_result['analysis']
                    result['score'] = ai_result['analysis'].get('score', 8)
                    
                    # Convert AI issues to standard format
                    ai_issues = ai_result['analysis'].get('issues', [])
                    for issue in ai_issues:
                        result['issues'].append({
                            'type': 'ai_insight',
                            'severity': 'medium',
                            'message': issue,
                            'line': 0,
                            'source': 'AI Analysis'
                        })
            
            # Calculate final score based on issues
            if result['issues']:
                critical_count = sum(1 for issue in result['issues'] if issue.get('severity') == 'critical')
                high_count = sum(1 for issue in result['issues'] if issue.get('severity') == 'high')
                medium_count = sum(1 for issue in result['issues'] if issue.get('severity') == 'medium')
                
                # Reduce score based on issues
                score_reduction = (critical_count * 3) + (high_count * 2) + (medium_count * 1)
                result['score'] = max(1, result['score'] - score_reduction)
            
            return result
            
        except Exception as e:
            logger.error(f"Single file analysis failed for {filename}: {str(e)}")
            return {
                'success': False,
                'filename': filename,
                'error': str(e)
            }
    
    def _analyze_python(self, content: str, filename: str) -> Dict[str, Any]:
        """Analyze Python code using pylint and bandit"""
        
        issues = []
        metrics = {}
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            try:
                # Run pylint for code quality
                pylint_result = subprocess.run(
                    ['pylint', '--output-format=json', '--disable=C0114,C0115,C0116', temp_file_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if pylint_result.stdout:
                    pylint_issues = json.loads(pylint_result.stdout)
                    for issue in pylint_issues:
                        issues.append({
                            'type': 'code_quality',
                            'severity': self._map_pylint_severity(issue.get('type', 'info')),
                            'message': issue.get('message', ''),
                            'line': issue.get('line', 0),
                            'column': issue.get('column', 0),
                            'source': 'Pylint'
                        })
                
                # Run bandit for security analysis
                bandit_result = subprocess.run(
                    ['bandit', '-f', 'json', temp_file_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if bandit_result.stdout:
                    bandit_data = json.loads(bandit_result.stdout)
                    for issue in bandit_data.get('results', []):
                        issues.append({
                            'type': 'security',
                            'severity': issue.get('issue_severity', 'medium').lower(),
                            'message': issue.get('issue_text', ''),
                            'line': issue.get('line_number', 0),
                            'source': 'Bandit'
                        })
                
                # Basic metrics
                lines = content.split('\n')
                metrics = {
                    'lines_of_code': len([line for line in lines if line.strip() and not line.strip().startswith('#')]),
                    'total_lines': len(lines),
                    'comment_lines': len([line for line in lines if line.strip().startswith('#')])
                }
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"Python analysis failed: {str(e)}")
            issues.append({
                'type': 'analysis_error',
                'severity': 'low',
                'message': f'Static analysis partially failed: {str(e)}',
                'line': 0,
                'source': 'System'
            })
        
        return {'issues': issues, 'metrics': metrics}
    
    def _analyze_javascript(self, content: str, filename: str) -> Dict[str, Any]:
        """Analyze JavaScript/TypeScript code using ESLint"""
        
        issues = []
        metrics = {}
        
        try:
            # Create temporary file
            file_ext = '.ts' if filename.endswith(('.ts', '.tsx')) else '.js'
            with tempfile.NamedTemporaryFile(mode='w', suffix=file_ext, delete=False) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            try:
                # Run ESLint
                eslint_result = subprocess.run(
                    ['npx', 'eslint', '--format=json', temp_file_path],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd='/home/ubuntu'  # Use a directory where eslint might be available
                )
                
                if eslint_result.stdout:
                    eslint_data = json.loads(eslint_result.stdout)
                    for file_result in eslint_data:
                        for message in file_result.get('messages', []):
                            issues.append({
                                'type': 'code_quality',
                                'severity': self._map_eslint_severity(message.get('severity', 1)),
                                'message': message.get('message', ''),
                                'line': message.get('line', 0),
                                'column': message.get('column', 0),
                                'source': 'ESLint'
                            })
                
                # Basic metrics
                lines = content.split('\n')
                metrics = {
                    'lines_of_code': len([line for line in lines if line.strip() and not line.strip().startswith('//')]),
                    'total_lines': len(lines),
                    'comment_lines': len([line for line in lines if line.strip().startswith('//')])
                }
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"JavaScript analysis failed: {str(e)}")
            # Add basic syntax check
            try:
                # Simple syntax validation
                if 'function' in content or 'const' in content or 'let' in content:
                    metrics = {
                        'lines_of_code': len([line for line in content.split('\n') if line.strip()]),
                        'total_lines': len(content.split('\n')),
                        'comment_lines': 0
                    }
            except:
                pass
        
        return {'issues': issues, 'metrics': metrics}
    
    def _map_pylint_severity(self, pylint_type: str) -> str:
        """Map pylint message types to severity levels"""
        mapping = {
            'error': 'high',
            'warning': 'medium',
            'refactor': 'low',
            'convention': 'low',
            'info': 'low'
        }
        return mapping.get(pylint_type.lower(), 'medium')
    
    def _map_eslint_severity(self, eslint_severity: int) -> str:
        """Map ESLint severity numbers to severity levels"""
        if eslint_severity == 2:
            return 'high'
        elif eslint_severity == 1:
            return 'medium'
        else:
            return 'low'
    
    def _combine_files_for_ai(self, files: List[Dict[str, Any]]) -> str:
        """Combine multiple files for AI analysis"""
        
        combined = "=== CODEBASE ANALYSIS ===\n\n"
        
        for file_info in files[:5]:  # Limit to first 5 files to avoid token limits
            combined += f"=== FILE: {file_info['name']} ===\n"
            combined += file_info['content'][:2000]  # Limit each file to 2000 chars
            if len(file_info['content']) > 2000:
                combined += "\n... (truncated)"
            combined += "\n\n"
        
        if len(files) > 5:
            combined += f"... and {len(files) - 5} more files\n"
        
        return combined
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported programming languages"""
        return list(set(self.supported_extensions.values()))
    
    def is_supported_file(self, filename: str) -> bool:
        """Check if file type is supported for analysis"""
        file_ext = os.path.splitext(filename)[1].lower()
        return file_ext in self.supported_extensions

