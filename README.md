# 🎨 Presentation Generator API

> AI-powered presentation generation service with flexible pricing and secure authentication

[![FastAPI](https://img.shields.io/badge/FastAPI-0.103.1-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](LICENSE)

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Architecture](#-architecture)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [API Reference](#-api-reference)
- [Examples](#-examples)
- [Support](#-support)

---

## ✨ Features

### 🎯 Core Features
- **AI-Powered Generation**: Automatic presentation creation using OpenAI GPT-4
- **Multiple Input Methods**: Support for JSON API and PDF file uploads
- **Flexible Slide Types**: Title, Content, Bullet Points, Two-Column, and Image slides
- **Async Processing**: Background task processing with Celery
- **Real-time Status**: Track generation progress with polling endpoints

### 🔐 Security
- **JWT Authentication**: Industry-standard token-based authentication
- **API Key Management**: Secure API key validation
- **CORS Support**: Configurable cross-origin resource sharing

### 💰 Pricing System
- **Flexible Tiers**: Multiple pricing packages with automatic discounts
- **Cost Calculator**: Real-time price calculation based on slide count
- **Public Pricing API**: Transparent pricing information

### 🚀 Performance
- **Docker Support**: Containerized deployment
- **Redis Caching**: Fast task queue and result backend
- **Scalable Architecture**: Horizontal scaling support

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose (recommended)
- OR Python 3.11+ and Redis

### Installation

#### Option 1: Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/presentation-generator.git
cd presentation-generator

# 2. Create environment file
cp .env.example .env

# 3. Configure your API keys
nano .env

# 4. Start services
docker-compose up -d

# 5. Access API
open http://localhost:8000/docs
```

#### Option 2: Local Development

```bash
# 1. Clone repository
git clone https://github.com/yourusername/presentation-generator.git
cd presentation-generator

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env

# 5. Start Redis
redis-server

# 6. Start Celery worker (new terminal)
celery -A celery_app worker --loglevel=info

# 7. Start API server (new terminal)
uvicorn app.main:app --reload

# 8. Access API
open http://localhost:8000/docs
```

---

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Base URL
```
Production: https://your-domain.com
Development: http://localhost:8000
```

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Client App    │
│  (Frontend/API) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │◄──── JWT Authentication
│   API Server    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌────────┐
│ Redis │ │ Celery │
│ Queue │ │ Worker │
└───────┘ └────┬───┘
              │
              ▼
         ┌──────────┐
         │  OpenAI  │
         │   API    │
         └──────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| API Framework | FastAPI 0.103.1 | High-performance REST API |
| Task Queue | Celery 5.3.4 | Async background processing |
| Message Broker | Redis 7.x | Task queue and caching |
| AI Engine | OpenAI GPT-4 | Content generation |
| Authentication | JWT (python-jose) | Secure token-based auth |
| Document Processing | python-pptx | PowerPoint generation |
| PDF Processing | PyPDF2 | PDF text extraction |

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Application
APP_NAME=Presentation-Generator

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
RESULT_BACKEND=redis://localhost:6379/0

# OpenAI API
OPENAI_API_KEY=sk-your-openai-api-key-here

# JWT Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys (JSON array format)
API_KEYS=["demo-api-key-12345","client-key-67890","production-key-abc123"]

# Storage
STORAGE_PATH=./storage
```

### Security Best Practices

⚠️ **Important**: Before deploying to production:

1. **Change SECRET_KEY**: Generate a strong random key
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Secure API Keys**: Use environment-specific keys
3. **Enable HTTPS**: Always use SSL/TLS in production
4. **Restrict CORS**: Update `allow_origins` in `main.py`
5. **Rotate Tokens**: Implement token refresh mechanism

---

## 🚢 Deployment

### Docker Production Deployment

```bash
# 1. Build production image
docker-compose -f docker-compose.prod.yml build

# 2. Deploy
docker-compose -f docker-compose.prod.yml up -d

# 3. Check status
docker-compose ps

# 4. View logs
docker-compose logs -f api
```

### Cloud Platform Deployments

#### Heroku
```bash
heroku create your-app-name
heroku addons:create heroku-redis:hobby-dev
heroku config:set SECRET_KEY=your-secret-key
heroku config:set API_KEYS='["key1","key2"]'
git push heroku main
```

#### Railway.app
1. Connect GitHub repository
2. Add Redis service
3. Configure environment variables
4. Deploy automatically

#### AWS/DigitalOcean
```bash
# Install Docker on server
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clone and deploy
git clone your-repo
cd presentation-generator
docker-compose up -d
```

---

## 📖 API Reference

### Authentication

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "api_key": "your-api-key-here"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

### Pricing

#### Get All Pricing Tiers
```http
GET /api/pricing/tiers
```

**Response:**
```json
[
  {
    "name": "Basic",
    "slides_count": 5,
    "price": 4.5,
    "currency": "USD",
    "description": "5 ta slide uchun (10% chegirma)"
  }
]
```

#### Calculate Price
```http
GET /api/pricing/calculate?num_slides=10
```

**Response:**
```json
{
  "num_slides": 10,
  "recommended_tier": "Standard",
  "price": 8.5,
  "currency": "USD",
  "discount": 15.0
}
```

---

### Presentations

#### Create Presentation
```http
POST /api/presentations
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "title": "AI and Machine Learning",
  "author": "John Doe",
  "slides": [
    {
      "type": "title",
      "title": "Introduction to AI",
      "content": "A comprehensive overview"
    },
    {
      "type": "bullet_points",
      "title": "Key Concepts",
      "bullet_points": [
        "Machine Learning",
        "Deep Learning",
        "Neural Networks"
      ]
    }
  ],
  "theme": "default"
}
```

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending"
}
```

#### Check Status
```http
GET /api/presentations/{task_id}
```

**Response (Completed):**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "file_url": "http://your-domain.com/download/file.pptx",
  "message": "Presentation generated successfully"
}
```

#### Create from PDF
```http
POST /api/presentations/from-pdf
Content-Type: multipart/form-data

pdf_file: [binary file]
title: "My Presentation"
author: "John Doe"
theme: "default"
num_slides: 10
```

---

## 💻 Examples

### JavaScript/TypeScript

```javascript
// 1. Login and get token
async function login() {
  const response = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ api_key: 'demo-api-key-12345' })
  });
  const { access_token } = await response.json();
  return access_token;
}

// 2. Create presentation
async function createPresentation(token) {
  const response = await fetch('http://localhost:8000/api/presentations', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      title: "My Presentation",
      author: "John Doe",
      slides: [
        {
          type: "title",
          title: "Welcome",
          content: "Introduction"
        }
      ],
      theme: "default"
    })
  });
  const { task_id } = await response.json();
  return task_id;
}

// 3. Poll for completion
async function waitForCompletion(taskId) {
  while (true) {
    const response = await fetch(
      `http://localhost:8000/api/presentations/${taskId}`
    );
    const status = await response.json();
    
    if (status.status === 'completed') {
      return status.file_url;
    } else if (status.status === 'failed') {
      throw new Error(status.message);
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}

// Usage
const token = await login();
const taskId = await createPresentation(token);
const fileUrl = await waitForCompletion(taskId);
console.log('Download:', fileUrl);
```

### Python

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# 1. Login
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"api_key": "demo-api-key-12345"}
)
token = response.json()["access_token"]

# 2. Create presentation
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    f"{BASE_URL}/api/presentations",
    headers=headers,
    json={
        "title": "My Presentation",
        "author": "John Doe",
        "slides": [
            {
                "type": "title",
                "title": "Welcome",
                "content": "Introduction"
            }
        ],
        "theme": "default"
    }
)
task_id = response.json()["task_id"]

# 3. Poll for completion
while True:
    response = requests.get(
        f"{BASE_URL}/api/presentations/{task_id}"
    )
    status = response.json()
    
    if status["status"] == "completed":
        print(f"Download: {status['file_url']}")
        break
    elif status["status"] == "failed":
        print(f"Error: {status['message']}")
        break
    
    time.sleep(2)
```

### cURL

```bash
# 1. Login
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"api_key": "demo-api-key-12345"}' \
  | jq -r '.access_token')

# 2. Create presentation
TASK_ID=$(curl -X POST http://localhost:8000/api/presentations \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Presentation",
    "author": "John Doe",
    "slides": [{
      "type": "title",
      "title": "Welcome",
      "content": "Introduction"
    }],
    "theme": "default"
  }' \
  | jq -r '.task_id')

# 3. Check status
curl http://localhost:8000/api/presentations/$TASK_ID
```

---

## 💰 Pricing Tiers

| Tier | Slides | Price | Discount | Per Slide |
|------|--------|-------|----------|-----------|
| Single | 1 | $1.00 | 0% | $1.00 |
| Basic | 5 | $4.50 | 10% | $0.90 |
| Standard | 10 | $8.50 | 15% | $0.85 |
| Premium | 20 | $16.00 | 20% | $0.80 |
| Enterprise | 50 | $35.00 | 30% | $0.70 |
| Custom | 50+ | Contact us | Negotiable | Varies |

---

## 🎨 Slide Types

### 1. Title Slide
```json
{
  "type": "title",
  "title": "Main Title",
  "content": "Subtitle text"
}
```

### 2. Content Slide
```json
{
  "type": "content",
  "title": "Slide Title",
  "content": "Paragraph text content..."
}
```

### 3. Bullet Points
```json
{
  "type": "bullet_points",
  "title": "Key Points",
  "bullet_points": ["Point 1", "Point 2", "Point 3"]
}
```

### 4. Two Column
```json
{
  "type": "two_column",
  "title": "Comparison",
  "column1": "Left content",
  "column2": "Right content"
}
```

### 5. Image Slide
```json
{
  "type": "image",
  "title": "Visual Content",
  "image_url": "https://example.com/image.jpg"
}
```

---

## 🧪 Testing

### Run Tests
```bash
# Unit tests
pytest

# Integration tests
pytest tests/integration/

# Coverage report
pytest --cov=app tests/
```

### Manual Testing
Use the provided HTTP test files:
- `test_main.http` - API endpoint tests
- Use VS Code REST Client extension

---

## 📊 Monitoring

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "presentation-generator",
  "version": "1.0.0"
}
```

### Logs
```bash
# Docker logs
docker-compose logs -f api
docker-compose logs -f worker

# Local logs
tail -f logs/app.log
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError: jose
```bash
pip install python-jose[cryptography]
docker-compose build --no-cache
```

#### 2. Redis Connection Error
```bash
# Check Redis status
docker-compose ps redis
redis-cli ping
```

#### 3. OpenAI API Error
- Verify API key in `.env`
- Check billing status
- Ensure sufficient credits

#### 4. File Not Found (404)
- Check `STORAGE_PATH` configuration
- Verify file permissions
- Ensure volume mounts in Docker

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Your Name** - *Initial work* - [@yourusername](https://github.com/yourusername)

---

## 📞 Support

### Documentation
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Contact
- Email: support@your-domain.com
- Telegram: [@your_username](https://t.me/your_username)
- Issues: [GitHub Issues](https://github.com/yourusername/presentation-generator/issues)

### Response Time
- Critical bugs: 24 hours
- Feature requests: 1 week
- General questions: 48 hours

---

## 🙏 Acknowledgments

- FastAPI framework
- OpenAI GPT-4
- Celery project
- Python community

---

## 📈 Roadmap

- [ ] User authentication with database
- [ ] Payment integration (Stripe/PayPal)
- [ ] Template customization
- [ ] Batch processing
- [ ] Webhook notifications
- [ ] Analytics dashboard
- [ ] Multi-language support

---

**Made with ❤️ using FastAPI and OpenAI**
