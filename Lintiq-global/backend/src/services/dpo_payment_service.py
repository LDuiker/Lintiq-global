"""
Simple DPO Group Payment Service for Botswana
Handles credit purchases and payment processing
"""

import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DPOPaymentService:
    """Simple DPO Group payment integration"""
    
    def __init__(self):
        self.company_token = os.getenv('DPO_COMPANY_TOKEN', '')
        self.service_type = os.getenv('DPO_SERVICE_TYPE', '3854')
        self.api_url = os.getenv('DPO_API_URL', 'https://secure.3gdirectpay.com')
        
    def is_available(self):
        """Check if DPO payment service is configured"""
        return bool(self.company_token)
    
    def get_credit_packages(self):
        """Get available credit packages with USD pricing"""
        return [
            {
                'id': 'credits_50',
                'name': '50 Credits',
                'credits': 50,
                'price': 299,  # $2.99 in cents
                'price_display': '$2.99',
                'description': 'Perfect for individual developers and vibe coders',
                'popular': False
            },
            {
                'id': 'credits_100',
                'name': '100 Credits',
                'credits': 100,
                'price': 499,  # $4.99 in cents
                'price_display': '$4.99',
                'description': 'Most popular choice for regular users',
                'popular': True
            },
            {
                'id': 'credits_250',
                'name': '250 Credits',
                'credits': 250,
                'price': 999,  # $9.99 in cents
                'price_display': '$9.99',
                'description': 'Great for small teams and heavy users',
                'popular': False
            },
            {
                'id': 'credits_500',
                'name': '500 Credits',
                'credits': 500,
                'price': 1799,  # $17.99 in cents
                'price_display': '$17.99',
                'description': 'Best value for enterprises and power users',
                'popular': False
            }
        ]
    
    def create_payment_token(self, amount, currency, reference, customer_email, customer_name, return_url, cancel_url):
        """Create DPO payment token"""
        try:
            # Convert amount from cents to dollars for DPO
            amount_dollars = amount / 100
            
            # Create XML request for DPO
            xml_data = f"""<?xml version="1.0" encoding="utf-8"?>
            <API3G>
                <CompanyToken>{self.company_token}</CompanyToken>
                <Request>createToken</Request>
                <Transaction>
                    <PaymentAmount>{amount_dollars:.2f}</PaymentAmount>
                    <PaymentCurrency>{currency}</PaymentCurrency>
                    <CompanyRef>{reference}</CompanyRef>
                    <RedirectURL>{return_url}</RedirectURL>
                    <BackURL>{cancel_url}</BackURL>
                    <CompanyRefUnique>0</CompanyRefUnique>
                    <PTL>5</PTL>
                </Transaction>
                <Services>
                    <Service>
                        <ServiceType>{self.service_type}</ServiceType>
                        <ServiceDescription>LintIQ Credits Purchase</ServiceDescription>
                        <ServiceDate>{datetime.now().strftime('%Y/%m/%d %H:%M')}</ServiceDate>
                    </Service>
                </Services>
            </API3G>"""
            
            # Send request to DPO
            response = requests.post(
                f"{self.api_url}/API/v6/",
                data=xml_data,
                headers={'Content-Type': 'application/xml'},
                timeout=30
            )
            
            if response.status_code == 200:
                # Parse XML response
                root = ET.fromstring(response.text)
                result = root.find('Result').text if root.find('Result') is not None else None
                
                if result == '000':  # Success
                    token = root.find('TransToken').text if root.find('TransToken') is not None else None
                    if token:
                        payment_url = f"{self.api_url}/payv2.php?ID={token}"
                        return {
                            'success': True,
                            'token': token,
                            'payment_url': payment_url
                        }
                else:
                    error_desc = root.find('ResultExplanation').text if root.find('ResultExplanation') is not None else 'Unknown error'
                    return {
                        'success': False,
                        'error': f'DPO Error: {error_desc}'
                    }
            else:
                return {
                    'success': False,
                    'error': f'HTTP Error: {response.status_code}'
                }
                
        except Exception as e:
            logger.error(f"DPO payment token creation failed: {str(e)}")
            return {
                'success': False,
                'error': 'Payment service temporarily unavailable'
            }
    
    def verify_payment(self, token):
        """Verify payment status with DPO"""
        try:
            xml_data = f"""<?xml version="1.0" encoding="utf-8"?>
            <API3G>
                <CompanyToken>{self.company_token}</CompanyToken>
                <Request>verifyToken</Request>
                <TransactionToken>{token}</TransactionToken>
            </API3G>"""
            
            response = requests.post(
                f"{self.api_url}/API/v6/",
                data=xml_data,
                headers={'Content-Type': 'application/xml'},
                timeout=30
            )
            
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                result = root.find('Result').text if root.find('Result') is not None else None
                
                if result == '000':  # Success
                    return {
                        'success': True,
                        'status': 'completed',
                        'transaction_approved': True
                    }
                else:
                    return {
                        'success': True,
                        'status': 'pending',
                        'transaction_approved': False
                    }
            else:
                return {
                    'success': False,
                    'error': f'Verification failed: {response.status_code}'
                }
                
        except Exception as e:
            logger.error(f"DPO payment verification failed: {str(e)}")
            return {
                'success': False,
                'error': 'Payment verification failed'
            }
    
    def simulate_purchase(self, package_id, user_id):
        """Simulate a successful purchase for testing"""
        packages = {pkg['id']: pkg for pkg in self.get_credit_packages()}
        package = packages.get(package_id)
        
        if not package:
            return {
                'success': False,
                'error': 'Invalid package ID'
            }
        
        # Generate a fake transaction ID
        transaction_id = f"SIM-{user_id}-{package_id}-{int(datetime.now().timestamp())}"
        
        return {
            'success': True,
            'credits_added': package['credits'],
            'amount_paid': package['price'],
            'transaction_id': transaction_id,
            'payment_method': 'simulation'
        }

