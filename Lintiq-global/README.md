# LintIQ - AI-Powered Code Analysis for Global Developers

> **Simple, Clean, and Powerful** - AI-powered code analysis with affordable USD pricing for developers and vibe coders worldwide.

## 🚀 Features

### Core Analysis
- **Multi-Language Support**: Python, JavaScript, TypeScript, React
- **Security Scanning**: Bandit for Python, ESLint for JavaScript/TypeScript
- **AI-Powered Insights**: OpenAI GPT-4 integration for intelligent recommendations
- **Real-time Analysis**: Fast processing with detailed reports

### Payment & Billing
- **Global Payment Support**: Credit cards, PayPal, and local payment methods
- **USD Pricing**: Transparent pricing in US Dollars
- **Credit System**: Pay-per-use model with credit packages
- **Flexible Options**: Monthly subscriptions or one-time credit purchases

### User Experience
- **Professional UI**: Modern React frontend with Tailwind CSS
- **Responsive Design**: Works on desktop and mobile devices
- **Demo Account**: Instant access with 100 credits
- **Real-time Updates**: Live analysis progress and results

## 🏗️ Architecture

```
lintiq-global/
├── backend/                 # Flask API server
│   ├── src/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── static/         # Frontend build output
│   │   └── main.py         # Application entry point
│   └── requirements.txt    # Python dependencies
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts
│   │   └── lib/           # Utilities and API client
│   └── package.json       # Node.js dependencies
├── render.yaml            # Render deployment config
└── .env.example          # Environment variables template
```

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/lintiq-global.git
cd lintiq-global
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

### 4. Frontend Setup (New Terminal)
```bash
cd frontend
npm install -g pnpm
pnpm install
pnpm run dev
```

### 5. Access Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

## 🌍 Deployment

### Render (Recommended)

1. **Connect Repository**
   - Fork this repository to your GitHub
   - Connect GitHub to Render
   - Create new Web Service

2. **Configure Environment**
   ```bash
   SECRET_KEY=your-32-character-secret
   OPENAI_API_KEY=sk-proj-your-openai-key
   DPO_COMPANY_TOKEN=your-dpo-token  # Optional for global deployment
   ```

3. **Deploy**
   - Render will automatically build and deploy
   - Build time: ~10-15 minutes
   - Your app will be live at: `https://your-app.onrender.com`

### Manual Deployment

```bash
# Build frontend
cd frontend
pnpm install
pnpm run build
cp -r dist/* ../backend/src/static/

# Deploy backend
cd ../backend
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:$PORT src.main:app
```

## 🔑 API Keys Setup

### OpenAI API Key
1. Visit: https://platform.openai.com
2. Create account and add payment method
3. Generate API key
4. Add to environment: `OPENAI_API_KEY=sk-proj-...`

### Payment Gateway (Optional)
For enhanced payment processing, you can configure DPO Group or other payment providers:

1. **DPO Group** (Recommended for African markets)
   - Contact: info@dpogroup.com
   - Get Company Token and Service Type
   - Add to environment variables

2. **Stripe** (Global markets)
   - Visit: https://stripe.com
   - Get API keys
   - Configure webhook endpoints

## 💰 Pricing Strategy

### Credit Packages (USD)
- **50 Credits**: $2.99 (6¢/credit)
- **100 Credits**: $4.99 (5¢/credit) ⭐ Most Popular
- **250 Credits**: $9.99 (4¢/credit)
- **500 Credits**: $17.99 (3.6¢/credit)

### Subscription Plans
- **Free**: $0/month - 10 analyses, basic features
- **Pro**: $4.99/month - Unlimited analyses, AI insights

### Cost Analysis
- **OpenAI Cost**: ~$0.02 per analysis
- **Revenue**: $0.036-0.06 per credit
- **Payment Fees**: 2.9% + $0.30 (Stripe)
- **Net Profit**: 40-60% margin

## 🛠️ Development

### Backend Development
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Run with auto-reload
FLASK_ENV=development python src/main.py
```

### Frontend Development
```bash
cd frontend
pnpm run dev --host

# Build for production
pnpm run build
```

### Testing
```bash
# Test backend API
curl http://localhost:5000/health

# Test demo analysis
curl -X POST http://localhost:5000/api/analysis/demo

# Test authentication
curl -X POST http://localhost:5000/api/auth/demo
```

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/demo` - Demo account access
- `POST /api/auth/verify` - Token verification

### Analysis
- `GET /api/analysis/capabilities` - Get supported languages
- `POST /api/analysis/analyze` - Analyze code files
- `POST /api/analysis/demo` - Demo analysis
- `GET /api/analysis/history` - Analysis history

### Payments
- `GET /api/payments/packages` - Credit packages
- `POST /api/payments/create-payment` - Create payment
- `POST /api/payments/verify-payment` - Verify payment
- `POST /api/payments/simulate-purchase` - Simulate purchase (testing)

### User
- `GET /api/user/profile` - User profile
- `PUT /api/user/profile` - Update profile
- `GET /api/user/stats` - User statistics

## 🔒 Security

### Authentication
- JWT tokens with 7-day expiration
- Secure password hashing with bcrypt
- Token-based API authentication

### Payment Security
- Secure payment processing with industry standards
- No credit card data stored locally
- Webhook verification for payment confirmation

### Code Analysis Security
- Temporary file processing
- No code stored permanently
- Secure API communication with OpenAI

## 🌍 Global Market Focus

### Target Customers
- **Individual Developers**: Freelancers and solo developers
- **Vibe Coders**: Side project enthusiasts and hobbyists
- **Small Teams**: Startups and small development teams
- **Students**: Computer science students and bootcamp graduates
- **Open Source**: Contributors to open source projects

### Competitive Advantages
- **Affordable Pricing**: 50-70% cheaper than SonarQube, CodeClimate
- **AI-Powered**: Advanced insights not available in basic tools
- **No Setup**: Cloud-based, instant access
- **Global Support**: 24/7 support for worldwide users
- **Flexible Payment**: Multiple payment options and currencies

### Marketing Channels
- **Developer Communities**: GitHub, Stack Overflow, Reddit
- **Social Media**: Twitter, LinkedIn, YouTube
- **Content Marketing**: Blog posts, tutorials, case studies
- **Partnerships**: Integration with popular dev tools
- **Referral Program**: Word-of-mouth growth

## 📈 Business Metrics

### Technical KPIs
- **Uptime**: >99.9% availability target
- **Response Time**: <2 seconds for analysis
- **Payment Success**: >95% with global payment methods
- **User Satisfaction**: Feature usage and retention rates

### Business KPIs
- **Monthly Recurring Revenue (MRR)**
- **Customer Acquisition Cost (CAC)**
- **Lifetime Value (LTV)**
- **Churn Rate**
- **Credit Usage Patterns**

## 🆘 Support

### Technical Support
- **Documentation**: Comprehensive guides included
- **GitHub Issues**: Bug reports and feature requests
- **Email**: support@lintiq.com
- **Community**: Developer discussions and forums

### Payment Support
- **Global Coverage**: Support for major payment methods
- **Multi-Currency**: USD, EUR, GBP support
- **Refund Policy**: 30-day money-back guarantee

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 🎯 Roadmap

### Short-term (3 months)
- [ ] Enhanced AI analysis models
- [ ] PDF report generation
- [ ] Team collaboration features
- [ ] Mobile app development

### Medium-term (6 months)
- [ ] IDE integrations (VS Code, IntelliJ)
- [ ] CI/CD pipeline integration
- [ ] Advanced security scanning
- [ ] Custom rule configuration

### Long-term (12 months)
- [ ] Enterprise features and SSO
- [ ] On-premise deployment options
- [ ] Custom AI models for specific languages
- [ ] Advanced analytics and reporting

---

**Built for developers worldwide, powered by AI** 🌍

For questions or support, contact: [support@lintiq.com](mailto:support@lintiq.com)

