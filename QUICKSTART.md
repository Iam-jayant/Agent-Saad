# ⚡ Quick Start Guide - Agent Saad

Get Agent Saad running in 5 minutes!

## 🚀 Installation

### Windows:
```bash
install.bat
```

### Mac/Linux:
```bash
chmod +x install.sh
./install.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Download the AI model (~250MB on first run)

## ⚙️ Configuration

1. Open the `.env` file in a text editor

2. Add your API credentials (get them from the Setup Guide if needed):

```bash
# Minimum Required for Testing
KEYWORDS=test,demo,example

# Add your real credentials for production
TWITTER_BEARER_TOKEN=your_token_here
REDDIT_CLIENT_ID=your_id_here
REDDIT_CLIENT_SECRET=your_secret_here
SLACK_BOT_TOKEN=xoxb-your-token-here
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

**Don't have API credentials yet?** You can still test the system - it will work with limited functionality.

## ▶️ Run the Application

### Windows:
```bash
start.bat
```

### Mac/Linux:
```bash
chmod +x start.sh
./start.sh
```

Or manually:
```bash
python run.py
```

## 🎯 Test the System

1. **Open Dashboard**: http://localhost:5000

2. **Click "Test Alerts"**: This will:
   - Create a sample alert in the dashboard
   - Send test Slack message (if configured)
   - Send test email (if configured)

3. **Test Sentiment Analysis**: In your terminal or using curl:
   ```bash
   curl -X POST http://localhost:5000/api/test/sentiment \
     -H "Content-Type: application/json" \
     -d "{\"text\": \"This product is terrible and buggy!\"}"
   ```

4. **Run Manual Monitor**: Click "Run Monitor Now" to search social media

## 📊 What You'll See

### Dashboard Features:
- **Statistics**: Total alerts, critical/high counts, 24-hour activity
- **Alert Feed**: All detected negative sentiment with:
  - Source (Twitter/Reddit)
  - Urgency level (Critical/High/Medium/Low)
  - Sentiment score
  - Recommended response
  - Link to original post

### Alert Colors:
- 🔴 **Red**: Critical urgency
- 🟠 **Orange**: High urgency
- 🟡 **Yellow**: Medium urgency
- 🔵 **Blue**: Low urgency

## 🔍 How to Use

### 1. Configure Your Keywords
Edit `.env` and set your brand/product names:
```bash
KEYWORDS=YourBrand,YourProduct,@YourHandle
```

### 2. Adjust Sensitivity
Change the sentiment threshold (range: -1 to 0):
```bash
SENTIMENT_THRESHOLD=-0.3  # Default (moderate)
SENTIMENT_THRESHOLD=-0.5  # Less sensitive (fewer alerts)
SENTIMENT_THRESHOLD=-0.1  # More sensitive (more alerts)
```

### 3. Set Check Frequency
How often to monitor social media:
```bash
CHECK_INTERVAL_MINUTES=15  # Default
CHECK_INTERVAL_MINUTES=5   # More frequent (uses more API calls)
CHECK_INTERVAL_MINUTES=60  # Less frequent
```

### 4. Monitor Running
The agent automatically monitors social media every X minutes (based on your setting).

You can also:
- **Manual Check**: Click "Run Monitor Now" in dashboard
- **View Logs**: Check `agent_saad.log` file
- **API Health**: Visit http://localhost:5000/health

## 🧪 Testing Without API Credentials

Even without Twitter/Reddit credentials, you can:

1. ✅ Test sentiment analysis
2. ✅ See the dashboard interface
3. ✅ Create test alerts
4. ✅ Test email/Slack (with those credentials)
5. ❌ Can't fetch real social media data

To test the full system:
- Get at least Twitter Bearer Token (easiest to obtain)
- Or Reddit Client ID/Secret (also free and easy)

## 📱 Slack Integration Test

If you configured Slack:

1. Make sure you invited the bot to your channel:
   ```
   /invite @Agent Saad
   ```

2. Click "Test Alerts" in dashboard

3. Check your Slack channel for the test message

## 📧 Email Integration Test

If you configured email:

1. Make sure you're using an **App Password** (not regular password) for Gmail

2. Click "Test Alerts" in dashboard

3. Check your inbox for the test email

## ⚠️ Common Issues

### "Module not found" Error
```bash
# Make sure you activated the virtual environment
# Windows:
venv\Scripts\activate.bat

# Mac/Linux:
source venv/bin/activate

# Then try again:
python run.py
```

### "Cannot connect to Twitter/Reddit"
- Check your API credentials in `.env`
- Remove any extra spaces or quotes
- See SETUP_GUIDE.md for how to get credentials

### "Slack/Email not working"
- Click "Test Alerts" to verify
- Check `agent_saad.log` for errors
- For Slack: invite bot to channel first
- For Gmail: use App Password, not regular password

### Model Download Slow
- First run downloads ~250MB model
- Requires internet connection
- Takes 2-5 minutes
- Subsequent runs are fast (model is cached)

## 🎓 Next Steps

1. **Read SETUP_GUIDE.md** for detailed API credential instructions
2. **Customize** sentiment thresholds and keywords
3. **Deploy** to a server for 24/7 monitoring
4. **Extend** with more platforms or features

## 📞 Need Help?

- Check `agent_saad.log` for detailed error messages
- Review SETUP_GUIDE.md for step-by-step instructions
- Test each component individually using the dashboard buttons
- Verify all credentials in `.env` are correct (no extra spaces!)

## 🎉 Success Checklist

- [ ] Dashboard loads at http://localhost:5000
- [ ] Test alert appears in dashboard
- [ ] Sentiment analysis test works
- [ ] Slack test message received (if configured)
- [ ] Email test received (if configured)
- [ ] Manual monitor run completes
- [ ] Auto-monitoring runs every X minutes

**You're all set! Agent Saad is now monitoring for negative sentiment. 🤖**

