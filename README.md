# 🤖 Agent Saad - AI-Powered Customer Sentiment Alert System

> **Real-time sentiment monitoring for social media mentions using state-of-the-art AI models**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Transformers](https://img.shields.io/badge/🤗_Transformers-4.40+-orange.svg)](https://huggingface.co/transformers/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Agent Saad is an intelligent AI agent that continuously monitors Twitter/X and Reddit for brand mentions, automatically analyzes sentiment using advanced AI models, and sends real-time alerts via Slack and Email when negative sentiment is detected.

---

## 🎯 What Problem Does It Solve?

**Problem:** Support teams miss early warning signs of negative sentiment spreading across social media platforms, leading to:
- Delayed responses to customer complaints
- Viral negative feedback going unnoticed
- Lost opportunities to turn unhappy customers around
- Difficulty prioritizing which issues need immediate attention

**Solution:** Agent Saad automatically:
- ✅ Monitors multiple social platforms 24/7
- ✅ Analyzes sentiment using AI (not just keywords)
- ✅ Prioritizes alerts by urgency (Critical → Low)
- ✅ Provides AI-generated response recommendations
- ✅ Sends real-time notifications to your team
- ✅ Tracks all feedback in a beautiful dashboard

---

## 🧠 AI Model & Accuracy

### Model: DistilBERT (SST-2 Fine-tuned)

**Model Name:** `distilbert-base-uncased-finetuned-sst-2-english`

**Why This Model?**
- ✅ **Fast:** Inference time ~100ms per text on CPU
- ✅ **Accurate:** 90%+ accuracy on sentiment classification
- ✅ **Free:** No API costs, runs locally
- ✅ **Lightweight:** 250MB model size
- ✅ **Battle-tested:** Used by thousands of companies in production

### Technical Details

**Architecture:**
- **Base Model:** DistilBERT (66M parameters)
- **Training:** Fine-tuned on Stanford Sentiment Treebank v2 (SST-2)
- **Task:** Binary sentiment classification (Positive/Negative)
- **Framework:** PyTorch via HuggingFace Transformers

**Performance Metrics:**
- **Accuracy:** 91.3% on SST-2 test set
- **F1 Score:** 0.913
- **Inference Speed:** ~100ms per text (CPU)
- **Memory Usage:** ~500MB RAM during operation

**How It Works:**
1. Text is tokenized using WordPiece tokenization
2. DistilBERT processes the tokens through 6 transformer layers
3. Classification head outputs probability distribution
4. Score is normalized to range [-1, 1] for urgency calculation

### Sentiment Analysis Pipeline

```
Input Text → Tokenization → DistilBERT Encoder → Classification Head → Sentiment Score
                                                                              ↓
                                                                    [-1.0 to +1.0]
                                                                              ↓
                                                              Urgency: CRITICAL/HIGH/MEDIUM/LOW
```

**Threshold System:**
- Score ≤ -0.7 → **CRITICAL** (Very negative with strong language)
- Score ≤ -0.3 → **HIGH** (Clearly negative sentiment)
- Score ≤ 0.0 → **MEDIUM** (Slightly negative)
- Score > 0.0 → **LOW** (Neutral or positive)

---

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask 3.0** - Web framework for API and dashboard
- **PyTorch 2.8** - Deep learning framework
- **HuggingFace Transformers 4.40+** - AI model library
- **APScheduler 3.10** - Background job scheduling

### AI/ML
- **DistilBERT** - Sentiment analysis model
- **Transformers Pipeline** - High-level inference API
- **Tokenizers** - Fast text tokenization

### Social Media APIs
- **Tweepy 4.15+** - Twitter/X API client
- **PRAW 7.7** - Reddit API wrapper

### Notifications
- **Slack SDK 3.26** - Slack bot integration
- **SMTP (smtplib)** - Email notifications

### Data Storage
- **SQLite** - Local database for alerts
- **Thread-safe connections** - Concurrent access handling

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with variables
- **Vanilla JavaScript** - No framework overhead
- **Inter Font** - Modern typography
- **CSS Grid & Flexbox** - Responsive layouts

### UI Features
- 🎨 **Dark/Light Mode** - Automatic theme switching
- ✨ **Smooth Animations** - CSS transitions and keyframes
- 📱 **Fully Responsive** - Mobile-first design
- 🎯 **Interactive** - Ripple effects, hover states
- 🔔 **Toast Notifications** - Real-time feedback
- 📊 **Animated Charts** - Progress bars and stats

---

## 🌟 Key Features

### 1. **Real-Time Monitoring**
- Continuous scanning of Twitter and Reddit
- Configurable check intervals (default: 15 minutes)
- Keyword-based search across multiple platforms

### 2. **AI-Powered Analysis**
- State-of-the-art sentiment analysis
- Context-aware urgency detection
- Engagement metrics consideration

### 3. **Smart Alerting**
- Multi-channel notifications (Slack + Email)
- Priority-based alert routing
- Duplicate detection and prevention

### 4. **Intelligent Recommendations**
- AI-generated response suggestions
- Issue-specific guidance
- Escalation recommendations

### 5. **Beautiful Dashboard**
- Modern, gradient-based design
- Real-time statistics
- Filterable alert feed
- Dark/Light mode toggle
- Smooth animations and transitions

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Agent-Saad.git
cd Agent-Saad

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file with your credentials:

```bash
# Twitter/X API
TWITTER_BEARER_TOKEN=your_bearer_token

# Reddit API
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=SaadMonitoring/1.0.0

# Email
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
ALERT_EMAIL_TO=alerts@yourcompany.com

# Slack
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_CHANNEL=#alerts

# Monitoring
KEYWORDS=your_brand,your_product
SENTIMENT_THRESHOLD=-0.3
CHECK_INTERVAL_MINUTES=15
```

### Run

```bash
python run.py
```

Open **http://localhost:5000** in your browser.

---

## 📊 Dashboard Features

### Statistics Cards
- **Total Alerts:** Cumulative count with trend indicator
- **Critical Alerts:** High-priority issues requiring immediate action
- **High Priority:** Important negative feedback
- **Last 24 Hours:** Recent activity tracking

### Alert Feed
- **Color-coded urgency** levels for quick identification
- **Source badges** (Twitter/Reddit)
- **Sentiment scores** with visual indicators
- **Recommended responses** for each alert
- **Direct links** to original posts
- **Filtering** by urgency and source

### Controls
- **Run Monitor Now:** Manual monitoring trigger
- **Test Alerts:** Verify Slack/Email integration
- **Refresh:** Update dashboard data
- **Auto-refresh:** Every 30 seconds

---

## 🎯 How Urgency Is Determined

```python
def determine_urgency(sentiment_score: float, engagement: int) -> str:
    """
    sentiment_score: Range from -1.0 (very negative) to +1.0 (very positive)
    engagement: Sum of likes, retweets, comments, upvotes
    """
    
    if sentiment_score <= -0.7:
        return 'CRITICAL' if engagement > 100 else 'HIGH'
    elif sentiment_score <= -0.3:
        return 'HIGH' if engagement > 50 else 'MEDIUM'
    elif sentiment_score <= 0:
        return 'LOW'
    else:
        return 'LOW'  # Positive sentiment
```

**Factors Considered:**
1. **Sentiment Score** - Primary factor from AI model
2. **Engagement Metrics** - Viral potential (likes, shares, upvotes)
3. **Content Analysis** - Specific issue detection (bug, billing, etc.)

---

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard UI |
| `/api/alerts` | GET | Fetch recent alerts |
| `/api/stats` | GET | Get statistics |
| `/api/alert/<id>/status` | PUT | Update alert status |
| `/api/test/sentiment` | POST | Test sentiment analysis |
| `/api/test/alerts` | POST | Send test notifications |
| `/api/monitor/run` | POST | Trigger manual monitoring |
| `/health` | GET | Health check |

---

## 📈 Performance

### Resource Usage
- **Memory:** ~500MB (AI model loaded)
- **CPU:** Low idle, spikes during analysis
- **Disk:** ~300MB (model cache) + database
- **Network:** API calls every 15 minutes (configurable)

### Throughput
- **Sentiment Analysis:** ~10 texts/second on CPU
- **Monitoring Capacity:** 100-1000 mentions/day
- **Alert Processing:** Real-time (<1 second)

### Scalability
- Current setup handles small to medium brands
- Can process 100+ mentions per monitoring cycle
- SQLite sufficient for <10K alerts
- Upgrade to PostgreSQL for higher volumes

---

## 🔐 Security & Privacy

### Data Handling
- ✅ No data sent to external APIs (except social media)
- ✅ Credentials stored locally in `.env`
- ✅ `.gitignore` prevents credential exposure
- ✅ SQL injection protection (parameterized queries)
- ✅ Duplicate detection prevents re-processing

### Best Practices
- Use environment variables for secrets
- Rotate API tokens regularly
- Enable HTTPS in production
- Set up proper authentication for dashboard
- Monitor logs for suspicious activity

---

## 🎓 Use Cases

### For Support Teams
- Catch escalating issues early
- Prioritize responses by urgency
- Track sentiment trends over time
- Reduce response time to complaints

### For Product Teams
- Identify bugs and UX issues quickly
- Understand customer pain points
- Track feature feedback
- Monitor competitor mentions

### For Marketing Teams
- Monitor brand reputation
- Track campaign sentiment
- Identify influencer complaints
- Respond to viral negative content

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions welcome! This project can be extended with:
- More social platforms (Facebook, Instagram, TikTok)
- Advanced analytics and trend visualization
- Automated response generation
- Multi-language sentiment analysis
- Custom model fine-tuning
- Integration with CRM systems

---

## 📞 Support

For issues or questions:
1. Check the logs in `agent_saad.log`
2. Review [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
3. Test each component using built-in test endpoints
4. Verify all credentials in `.env`

---

## 🎉 Acknowledgments

- **HuggingFace** for Transformers library and pre-trained models
- **DistilBERT authors** for the efficient transformer architecture
- **SST-2 dataset** for sentiment training data
- **Open source community** for amazing tools and libraries

---

**Built with ❤️ for customer support teams worldwide**

*Protect your brand reputation with AI-powered sentiment monitoring*
