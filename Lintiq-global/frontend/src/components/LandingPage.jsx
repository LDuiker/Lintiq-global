/**
 * LandingPage Component - Global version with USD pricing
 * Targeting developers and vibe coders worldwide
 */

import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Code, 
  Shield, 
  Zap, 
  Brain, 
  CheckCircle, 
  Star,
  ArrowRight,
  Globe,
  CreditCard,
  Users,
  TrendingUp
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const LandingPage = () => {
  const { demoLogin } = useAuth();
  const navigate = useNavigate();

  const handleDemoLogin = async () => {
    const result = await demoLogin();
    if (result.success) {
      navigate('/dashboard');
    }
  };

  const features = [
    {
      icon: <Code className="h-8 w-8 text-blue-600" />,
      title: "Multi-Language Support",
      description: "Analyze Python, JavaScript, TypeScript, and React code with comprehensive linting rules."
    },
    {
      icon: <Shield className="h-8 w-8 text-green-600" />,
      title: "Security Scanning",
      description: "Detect security vulnerabilities and potential threats in your codebase automatically."
    },
    {
      icon: <Brain className="h-8 w-8 text-purple-600" />,
      title: "AI-Powered Insights",
      description: "Get intelligent recommendations and code improvements powered by advanced AI models."
    },
    {
      icon: <Zap className="h-8 w-8 text-yellow-600" />,
      title: "Lightning Fast",
      description: "Get analysis results in seconds with our optimized processing pipeline."
    }
  ];

  const pricingPlans = [
    {
      name: "Free",
      price: "$0",
      period: "/month",
      description: "Perfect for getting started",
      features: [
        "10 analyses per month",
        "Basic code analysis",
        "Security scanning",
        "Community support"
      ],
      popular: false,
      buttonText: "Get Started Free",
      buttonVariant: "outline"
    },
    {
      name: "Pro",
      price: "$4.99",
      period: "/month",
      description: "For serious developers and vibe coders",
      features: [
        "Unlimited analyses",
        "AI-powered insights",
        "Priority support",
        "Advanced security scanning",
        "PDF reports",
        "Team collaboration"
      ],
      popular: true,
      buttonText: "Start Pro Trial",
      buttonVariant: "default"
    }
  ];

  const stats = [
    { label: "Code Files Analyzed", value: "10,000+" },
    { label: "Security Issues Found", value: "2,500+" },
    { label: "Developer Hours Saved", value: "1,200+" },
    { label: "Languages Supported", value: "5+" }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Code className="h-6 w-6 text-white" />
              </div>
              <span className="text-2xl font-bold text-gray-900">LintIQ</span>
              <Badge variant="secondary" className="ml-2">Global</Badge>
            </div>
            
            <div className="flex items-center space-x-4">
              <Button variant="ghost" onClick={() => navigate('/login')}>
                Sign In
              </Button>
              <Button onClick={() => navigate('/register')}>
                Get Started
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <div className="text-center">
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              AI-Powered Code Analysis for{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                Global Developers
              </span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Lint, analyze, and improve your code with advanced AI insights. 
              Perfect for developers, vibe coders, and teams worldwide who want cleaner, more secure code.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" onClick={handleDemoLogin} className="text-lg px-8 py-3">
                Try Demo Now
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button size="lg" variant="outline" onClick={() => navigate('/register')} className="text-lg px-8 py-3">
                Start Free Trial
              </Button>
            </div>
            <p className="text-sm text-gray-500 mt-4">
              No credit card required • 10 free analyses • Instant setup
            </p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Powerful Features for Modern Development
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Everything you need to write better, more secure, and more maintainable code
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-center mb-4">
                    {feature.icon}
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-3xl font-bold text-blue-600 mb-2">{stat.value}</div>
                <div className="text-gray-600">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Simple, Transparent Pricing
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Choose the plan that works for you. Affordable pricing for developers worldwide.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {pricingPlans.map((plan, index) => (
              <Card key={index} className={`relative ${plan.popular ? 'ring-2 ring-blue-500 scale-105' : ''}`}>
                {plan.popular && (
                  <Badge className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-blue-500">
                    <Star className="h-3 w-3 mr-1" />
                    Most Popular
                  </Badge>
                )}
                <CardHeader className="text-center">
                  <CardTitle className="text-2xl">{plan.name}</CardTitle>
                  <div className="mt-4">
                    <span className="text-4xl font-bold">{plan.price}</span>
                    <span className="text-gray-600">{plan.period}</span>
                  </div>
                  <CardDescription>{plan.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3 mb-6">
                    {plan.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-center">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-3" />
                        <span className="text-gray-600">{feature}</span>
                      </li>
                    ))}
                  </ul>
                  <Button 
                    className="w-full" 
                    variant={plan.buttonVariant}
                    onClick={() => navigate('/register')}
                  >
                    {plan.buttonText}
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Credit Packages */}
          <div className="mt-16">
            <div className="text-center mb-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Pay-As-You-Go Credits</h3>
              <p className="text-gray-600">Perfect for occasional users and project-based work</p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
              <Card className="text-center">
                <CardHeader>
                  <CardTitle className="text-lg">Starter</CardTitle>
                  <div className="text-3xl font-bold text-blue-600">$2.99</div>
                  <CardDescription>50 Credits</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Perfect for individual developers</p>
                  <Button variant="outline" className="w-full" onClick={() => navigate('/register')}>
                    Buy Credits
                  </Button>
                </CardContent>
              </Card>

              <Card className="text-center border-blue-500 border-2">
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <Badge className="bg-blue-500 text-white">Most Popular</Badge>
                </div>
                <CardHeader>
                  <CardTitle className="text-lg">Popular</CardTitle>
                  <div className="text-3xl font-bold text-blue-600">$4.99</div>
                  <CardDescription>100 Credits</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Best value for regular users</p>
                  <Button className="w-full" onClick={() => navigate('/register')}>
                    Buy Credits
                  </Button>
                </CardContent>
              </Card>

              <Card className="text-center">
                <CardHeader>
                  <CardTitle className="text-lg">Team</CardTitle>
                  <div className="text-3xl font-bold text-blue-600">$9.99</div>
                  <CardDescription>250 Credits</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Great for small teams</p>
                  <Button variant="outline" className="w-full" onClick={() => navigate('/register')}>
                    Buy Credits
                  </Button>
                </CardContent>
              </Card>

              <Card className="text-center">
                <CardHeader>
                  <CardTitle className="text-lg">Enterprise</CardTitle>
                  <div className="text-3xl font-bold text-blue-600">$17.99</div>
                  <CardDescription>500 Credits</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Best value for power users</p>
                  <Button variant="outline" className="w-full" onClick={() => navigate('/register')}>
                    Buy Credits
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Global Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Built for Global Developers
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Whether you're a solo developer, part of a team, or a vibe coder working on side projects
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="text-center">
              <CardHeader>
                <Globe className="h-12 w-12 text-blue-600 mx-auto mb-4" />
                <CardTitle>Worldwide Access</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Available globally with fast processing and reliable uptime for developers everywhere.
                </p>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <CreditCard className="h-12 w-12 text-green-600 mx-auto mb-4" />
                <CardTitle>Flexible Payments</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Multiple payment options including credit cards, PayPal, and local payment methods.
                </p>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <Users className="h-12 w-12 text-purple-600 mx-auto mb-4" />
                <CardTitle>Community Driven</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Join thousands of developers worldwide who trust LintIQ for their code analysis needs.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="container mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-4">
            Ready to Improve Your Code?
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Join thousands of developers worldwide who use LintIQ to write better, more secure code.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" variant="secondary" onClick={handleDemoLogin} className="text-lg px-8 py-3">
              Try Demo Now
            </Button>
            <Button size="lg" variant="outline" onClick={() => navigate('/register')} className="text-lg px-8 py-3 bg-white text-blue-600 hover:bg-gray-100">
              Start Free Trial
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <Code className="h-5 w-5 text-white" />
                </div>
                <span className="text-xl font-bold">LintIQ</span>
              </div>
              <p className="text-gray-400">
                AI-powered code analysis for developers worldwide.
              </p>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Features</a></li>
                <li><a href="#" className="hover:text-white">Pricing</a></li>
                <li><a href="#" className="hover:text-white">API</a></li>
                <li><a href="#" className="hover:text-white">Documentation</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">About</a></li>
                <li><a href="#" className="hover:text-white">Blog</a></li>
                <li><a href="#" className="hover:text-white">Careers</a></li>
                <li><a href="#" className="hover:text-white">Contact</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Help Center</a></li>
                <li><a href="#" className="hover:text-white">Community</a></li>
                <li><a href="#" className="hover:text-white">Status</a></li>
                <li><a href="#" className="hover:text-white">Privacy</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 LintIQ. All rights reserved. Made for developers worldwide.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;

