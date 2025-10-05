import tweepy
import logging
from typing import List, Dict
from config import Config

logger = logging.getLogger(__name__)

class TwitterMonitor:
    def __init__(self):
        self.client = None
        self.setup_client()
    
    def setup_client(self):
        """Setup Twitter API client"""
        try:
            if Config.TWITTER_BEARER_TOKEN:
                self.client = tweepy.Client(
                    bearer_token=Config.TWITTER_BEARER_TOKEN,
                    consumer_key=Config.TWITTER_API_KEY,
                    consumer_secret=Config.TWITTER_API_SECRET,
                    access_token=Config.TWITTER_ACCESS_TOKEN,
                    access_token_secret=Config.TWITTER_ACCESS_SECRET,
                    wait_on_rate_limit=True
                )
                logger.info("Twitter client initialized successfully")
            else:
                logger.warning("Twitter API credentials not configured")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {e}")
    
    def search_mentions(self, keywords: List[str], max_results: int = 10) -> List[Dict]:
        """
        Search for tweets mentioning keywords
        
        Args:
            keywords: List of keywords to search for
            max_results: Maximum number of results to return
        
        Returns:
            List of tweet data dictionaries
        """
        if not self.client:
            logger.warning("Twitter client not initialized")
            return []
        
        tweets_data = []
        
        try:
            # Build search query
            query = ' OR '.join([f'"{keyword}"' for keyword in keywords if keyword.strip()])
            query += ' -is:retweet'  # Exclude retweets
            
            if not query or query == ' -is:retweet':
                logger.warning("No valid keywords for Twitter search")
                return []
            
            # Search recent tweets
            response = self.client.search_recent_tweets(
                query=query,
                max_results=min(max_results, 100),
                tweet_fields=['created_at', 'public_metrics', 'author_id'],
                expansions=['author_id'],
                user_fields=['username']
            )
            
            if not response.data:
                logger.info("No tweets found")
                return []
            
            # Create user mapping
            users = {}
            if response.includes and 'users' in response.includes:
                users = {user.id: user.username for user in response.includes['users']}
            
            for tweet in response.data:
                author_username = users.get(tweet.author_id, 'unknown')
                
                tweets_data.append({
                    'id': str(tweet.id),
                    'text': tweet.text,
                    'author': f"@{author_username}",
                    'created_at': tweet.created_at.isoformat() if tweet.created_at else None,
                    'url': f"https://twitter.com/{author_username}/status/{tweet.id}",
                    'engagement': (
                        tweet.public_metrics.get('like_count', 0) +
                        tweet.public_metrics.get('retweet_count', 0) +
                        tweet.public_metrics.get('reply_count', 0)
                    ) if tweet.public_metrics else 0
                })
            
            logger.info(f"Found {len(tweets_data)} tweets")
            return tweets_data
            
        except tweepy.TweepyException as e:
            logger.error(f"Twitter API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Error searching tweets: {e}")
            return []
    
    def get_user_tweets(self, username: str, max_results: int = 10) -> List[Dict]:
        """
        Get recent tweets from a specific user
        
        Args:
            username: Twitter username (without @)
            max_results: Maximum number of results
        
        Returns:
            List of tweet data dictionaries
        """
        if not self.client:
            return []
        
        try:
            # Get user ID
            user = self.client.get_user(username=username)
            if not user.data:
                return []
            
            user_id = user.data.id
            
            # Get user's tweets
            response = self.client.get_users_tweets(
                id=user_id,
                max_results=max_results,
                tweet_fields=['created_at', 'public_metrics']
            )
            
            if not response.data:
                return []
            
            tweets_data = []
            for tweet in response.data:
                tweets_data.append({
                    'id': str(tweet.id),
                    'text': tweet.text,
                    'author': f"@{username}",
                    'created_at': tweet.created_at.isoformat() if tweet.created_at else None,
                    'url': f"https://twitter.com/{username}/status/{tweet.id}",
                    'engagement': (
                        tweet.public_metrics.get('like_count', 0) +
                        tweet.public_metrics.get('retweet_count', 0)
                    ) if tweet.public_metrics else 0
                })
            
            return tweets_data
            
        except Exception as e:
            logger.error(f"Error getting user tweets: {e}")
            return []

