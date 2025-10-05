from flask import Flask, render_template, jsonify, request
import logging
from datetime import datetime
from app.database.db import Database
from app.models.sentiment import SentimentAnalyzer
from app.monitors.twitter_monitor import TwitterMonitor
from app.monitors.reddit_monitor import RedditMonitor
from app.alerts.slack_alert import SlackAlerter
from app.alerts.email_alert import EmailAlerter
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='../static')
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Initialize components
db = Database(Config.DATABASE_PATH)
sentiment_analyzer = SentimentAnalyzer()
twitter_monitor = TwitterMonitor()
reddit_monitor = RedditMonitor()
slack_alerter = SlackAlerter()
email_alerter = EmailAlerter()

@app.route('/')
def dashboard():
    """Render the main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/alerts')
def get_alerts():
    """Get recent alerts"""
    try:
        limit = request.args.get('limit', 50, type=int)
        alerts = db.get_recent_alerts(limit=limit)
        return jsonify({
            'success': True,
            'alerts': alerts,
            'count': len(alerts)
        })
    except Exception as e:
        logger.error(f"Error fetching alerts: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get dashboard statistics"""
    try:
        stats = db.get_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/alert/<int:alert_id>/status', methods=['PUT'])
def update_alert_status(alert_id):
    """Update alert status"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if status not in ['new', 'in_progress', 'resolved', 'ignored']:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400
        
        db.update_alert_status(alert_id, status)
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error updating alert status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test/sentiment', methods=['POST'])
def test_sentiment():
    """Test sentiment analysis"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
        
        result = sentiment_analyzer.analyze(text)
        urgency = sentiment_analyzer.determine_urgency(result['normalized_score'])
        recommendation = sentiment_analyzer.generate_response_recommendation(text, result['label'])
        
        return jsonify({
            'success': True,
            'sentiment': result,
            'urgency': urgency,
            'recommendation': recommendation
        })
    except Exception as e:
        logger.error(f"Error testing sentiment: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test/alerts', methods=['POST'])
def test_alerts():
    """Test alert system - sends a test alert via Slack and Email"""
    try:
        logger.info("Testing alert systems...")
        
        # Create test alert
        test_alert = {
            'source': 'Test',
            'content': 'This is a test alert from Agent Saad. The system is working correctly!',
            'author': 'Agent Saad Testing',
            'url': 'http://localhost:5000',
            'sentiment_score': -0.65,
            'sentiment_label': 'NEGATIVE',
            'urgency_level': 'HIGH',
            'recommended_response': 'This is a test alert. No action required.'
        }
        
        # Save to database
        alert_id = db.add_alert(test_alert)
        
        # Send alerts
        slack_sent = slack_alerter.send_test_alert()
        email_sent = email_alerter.send_test_alert()
        
        # Mark as notified
        if slack_sent or email_sent:
            db.mark_as_notified(alert_id)
        
        return jsonify({
            'success': True,
            'alert_id': alert_id,
            'slack_sent': slack_sent,
            'email_sent': email_sent,
            'message': 'Test alert sent successfully!'
        })
    except Exception as e:
        logger.error(f"Error testing alerts: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/monitor/run', methods=['POST'])
def run_monitor():
    """Manually trigger a monitoring check"""
    try:
        from app.agent import process_monitoring_cycle
        results = process_monitoring_cycle()
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        logger.error(f"Error running monitor: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Agent Saad'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)

