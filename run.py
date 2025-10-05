"""
Agent Saad - Customer Sentiment Alert System
Main entry point for running the application
"""

import logging
import sys
from app.main import app
from app.agent import start_scheduled_monitoring
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('agent_saad.log')
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    logger.info("="*60)
    logger.info("Starting Agent Saad - Customer Sentiment Alert System")
    logger.info("="*60)
    
    try:
        # Start scheduled monitoring
        scheduler = start_scheduled_monitoring()
        
        # Run Flask app
        logger.info(f"Starting web dashboard on http://localhost:{Config.PORT}")
        logger.info(f"Monitoring keywords: {Config.KEYWORDS}")
        logger.info(f"Check interval: {Config.CHECK_INTERVAL_MINUTES} minutes")
        logger.info(f"Sentiment threshold: {Config.SENTIMENT_THRESHOLD}")
        logger.info("="*60)
        
        # Run the Flask application
        app.run(
            host='0.0.0.0',
            port=Config.PORT,
            debug=Config.DEBUG,
            use_reloader=False  # Disable reloader to prevent scheduler duplication
        )
        
    except KeyboardInterrupt:
        logger.info("Shutting down Agent Saad...")
        scheduler.shutdown()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()

