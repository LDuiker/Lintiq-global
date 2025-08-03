"""
Payment routes for LintIQ
Handles DPO Group payment integration with USD pricing
"""

import time
import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User
from ..services.dpo_payment_service import DPOPaymentService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
payments_bp = Blueprint('payments', __name__)

# Initialize payment service
payment_service = DPOPaymentService()

@payments_bp.route('/packages', methods=['GET'])
def get_credit_packages():
    """Get available credit packages"""
    try:
        packages = payment_service.get_credit_packages()
        
        return jsonify({
            'success': True,
            'packages': packages,
            'payment_available': payment_service.is_available(),
            'currency': 'USD',
            'gateway': 'DPO Group'
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting credit packages: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to load credit packages'
        }), 500

@payments_bp.route('/create-payment', methods=['POST'])
@jwt_required()
def create_payment():
    """Create a payment for credit purchase"""
    try:
        data = request.get_json()
        package_id = data.get('package_id')
        
        if not package_id:
            return jsonify({
                'success': False,
                'error': 'Package ID is required'
            }), 400
        
        # Get current user
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Get package details
        packages = payment_service.get_credit_packages()
        package = next((p for p in packages if p['id'] == package_id), None)
        
        if not package:
            return jsonify({
                'success': False,
                'error': 'Invalid package ID'
            }), 400
        
        # Create payment with DPO Group
        reference = f"LINTIQ-{user.id}-{int(time.time())}"
        payment_result = payment_service.create_payment_token(
            amount=package['price'],
            currency='USD',
            reference=reference,
            customer_email=user.email,
            customer_name=user.username,
            return_url=f"{request.host_url}payment/success",
            cancel_url=f"{request.host_url}payment/cancel"
        )
        
        if payment_result['success']:
            return jsonify({
                'success': True,
                'payment_url': payment_result['payment_url'],
                'token': payment_result['token'],
                'package': package,
                'reference': reference
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': payment_result['error']
            }), 500
            
    except Exception as e:
        logger.error(f"Error creating payment: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to create payment'
        }), 500

@payments_bp.route('/verify-payment', methods=['POST'])
@jwt_required()
def verify_payment():
    """Verify payment status with DPO Group"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({
                'success': False,
                'error': 'Payment token is required'
            }), 400
        
        # Verify payment with DPO
        verification_result = payment_service.verify_payment(token)
        
        if verification_result['success'] and verification_result['status'] == 'paid':
            # Get current user
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if user:
                # Add credits to user account
                credits_to_add = verification_result.get('credits', 0)
                user.add_credits(credits_to_add)
                
                return jsonify({
                    'success': True,
                    'status': 'paid',
                    'credits_added': credits_to_add,
                    'new_balance': user.credits
                }), 200
        
        return jsonify({
            'success': True,
            'status': verification_result.get('status', 'pending')
        }), 200
        
    except Exception as e:
        logger.error(f"Error verifying payment: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to verify payment'
        }), 500

@payments_bp.route('/simulate-purchase', methods=['POST'])
@jwt_required()
def simulate_purchase():
    """Simulate credit purchase for testing (demo purposes)"""
    try:
        data = request.get_json()
        package_id = data.get('package_id')
        
        if not package_id:
            return jsonify({
                'success': False,
                'error': 'Package ID is required'
            }), 400
        
        # Get current user
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Get package details
        packages = payment_service.get_credit_packages()
        package = next((p for p in packages if p['id'] == package_id), None)
        
        if not package:
            return jsonify({
                'success': False,
                'error': 'Invalid package ID'
            }), 400
        
        # Simulate successful purchase
        credits_to_add = package['credits']
        user.add_credits(credits_to_add)
        
        # Add to total spent (for demo purposes)
        user.total_spent = (user.total_spent or 0) + package['price']
        user.save()
        
        return jsonify({
            'success': True,
            'credits_added': credits_to_add,
            'new_balance': user.credits,
            'package': package,
            'message': f"Successfully added {credits_to_add} credits to your account!"
        }), 200
        
    except Exception as e:
        logger.error(f"Error simulating purchase: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to simulate purchase'
        }), 500

@payments_bp.route('/webhook', methods=['POST'])
def payment_webhook():
    """Handle DPO Group payment webhooks"""
    try:
        # Get webhook data
        data = request.get_json() or request.form.to_dict()
        
        # Verify webhook authenticity (implement based on DPO documentation)
        # This is a simplified version - implement proper verification
        
        token = data.get('TransToken')
        status = data.get('Result')
        reference = data.get('CompanyRef')
        
        if token and status == '000':  # 000 = successful payment in DPO
            # Find user by reference
            user_id = reference.split('-')[1] if '-' in reference else None
            
            if user_id:
                user = User.query.get(int(user_id))
                if user:
                    # Verify payment and add credits
                    verification_result = payment_service.verify_payment(token)
                    
                    if verification_result['success']:
                        credits_to_add = verification_result.get('credits', 0)
                        user.add_credits(credits_to_add)
                        
                        logger.info(f"Webhook: Added {credits_to_add} credits to user {user_id}")
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({'success': False}), 500

