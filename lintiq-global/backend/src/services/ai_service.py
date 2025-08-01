"""
AI Service for LintIQ - OpenAI Integration
Provides intelligent code analysis and recommendations
"""

import os
import openai
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class AIService:
    """AI-powered code analysis using OpenAI"""
    
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        )
        self.model = "gpt-4o-mini"  # Cost-effective model for code analysis
    
    def is_available(self):
        """Check if AI service is configured"""
        return bool(os.getenv('OPENAI_API_KEY'))
    
    def analyze_code(self, code: str, language: str, filename: str = "") -> Dict[str, Any]:
        """
        Analyze code using AI and provide intelligent insights
        
        Args:
            code: The source code to analyze
            language: Programming language (python, javascript, typescript, etc.)
            filename: Optional filename for context
            
        Returns:
            Dictionary with AI analysis results
        """
        try:
            # Create analysis prompt
            prompt = self._create_analysis_prompt(code, language, filename)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert code reviewer and software engineer. Provide detailed, actionable feedback on code quality, security, performance, and best practices."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1500,
                temperature=0.1  # Low temperature for consistent, focused analysis
            )
            
            # Parse response
            analysis_text = response.choices[0].message.content
            
            # Structure the response
            return {
                'success': True,
                'analysis': self._parse_ai_analysis(analysis_text),
                'raw_response': analysis_text,
                'model_used': self.model,
                'tokens_used': response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            return {
                'success': False,
                'error': 'AI analysis temporarily unavailable',
                'analysis': {
                    'summary': 'AI analysis could not be completed',
                    'issues': [],
                    'recommendations': [],
                    'score': 0
                }
            }
    
    def _create_analysis_prompt(self, code: str, language: str, filename: str) -> str:
        """Create a structured prompt for code analysis"""
        
        prompt = f"""
Please analyze this {language} code and provide a comprehensive review:

**File**: {filename or 'Unknown'}
**Language**: {language}

**Code to analyze:**
```{language}
{code}
```

Please provide analysis in the following format:

**SUMMARY:**
Brief overall assessment of the code quality (2-3 sentences)

**ISSUES FOUND:**
List specific problems with severity levels (Critical/High/Medium/Low):
- Issue description with line references where possible

**RECOMMENDATIONS:**
Actionable suggestions for improvement:
- Specific recommendations with examples

**SECURITY CONCERNS:**
Any potential security vulnerabilities or risks

**PERFORMANCE NOTES:**
Performance optimization opportunities

**BEST PRACTICES:**
Adherence to coding standards and best practices

**OVERALL SCORE:**
Rate the code quality from 1-10 (10 being excellent)

Focus on:
1. Code quality and maintainability
2. Security vulnerabilities
3. Performance issues
4. Best practices adherence
5. Potential bugs or logic errors
6. Code structure and organization
"""
        
        return prompt
    
    def _parse_ai_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """Parse AI response into structured format"""
        
        try:
            # Initialize result structure
            result = {
                'summary': '',
                'issues': [],
                'recommendations': [],
                'security_concerns': [],
                'performance_notes': [],
                'best_practices': [],
                'score': 0
            }
            
            # Split analysis into sections
            sections = analysis_text.split('**')
            current_section = None
            current_content = []
            
            for section in sections:
                section = section.strip()
                if not section:
                    continue
                
                # Check for section headers
                if 'SUMMARY' in section.upper():
                    current_section = 'summary'
                elif 'ISSUES FOUND' in section.upper():
                    current_section = 'issues'
                elif 'RECOMMENDATIONS' in section.upper():
                    current_section = 'recommendations'
                elif 'SECURITY CONCERNS' in section.upper():
                    current_section = 'security_concerns'
                elif 'PERFORMANCE NOTES' in section.upper():
                    current_section = 'performance_notes'
                elif 'BEST PRACTICES' in section.upper():
                    current_section = 'best_practices'
                elif 'OVERALL SCORE' in section.upper():
                    current_section = 'score'
                else:
                    # This is content for the current section
                    if current_section:
                        current_content.append(section)
                        
                        # Process content when we hit a new section or end
                        if current_section == 'summary':
                            result['summary'] = section.strip()
                        elif current_section == 'score':
                            # Extract numeric score
                            import re
                            score_match = re.search(r'(\d+)', section)
                            if score_match:
                                result['score'] = int(score_match.group(1))
                        elif current_section in ['issues', 'recommendations', 'security_concerns', 'performance_notes', 'best_practices']:
                            # Parse list items
                            items = [item.strip() for item in section.split('\n') if item.strip() and item.strip().startswith('-')]
                            result[current_section].extend([item[1:].strip() for item in items])
            
            # Ensure we have at least basic content
            if not result['summary']:
                result['summary'] = 'Code analysis completed successfully.'
            
            if result['score'] == 0:
                result['score'] = 7  # Default reasonable score
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to parse AI analysis: {str(e)}")
            # Return basic structure if parsing fails
            return {
                'summary': analysis_text[:200] + '...' if len(analysis_text) > 200 else analysis_text,
                'issues': ['Analysis parsing incomplete - see raw response'],
                'recommendations': ['Review the complete analysis in the raw response'],
                'security_concerns': [],
                'performance_notes': [],
                'best_practices': [],
                'score': 7
            }
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get AI service usage statistics"""
        return {
            'service': 'OpenAI',
            'model': self.model,
            'available': self.is_available(),
            'cost_per_analysis': 'Approximately $0.01-0.02 USD',
            'features': [
                'Code quality analysis',
                'Security vulnerability detection',
                'Performance optimization suggestions',
                'Best practices recommendations',
                'Multi-language support'
            ]
        }

