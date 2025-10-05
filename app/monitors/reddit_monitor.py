import praw
import logging
from typing import List, Dict
from config import Config
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class RedditMonitor:
    def __init__(self):
        self.reddit = None
        self.setup_client()
    
    def setup_client(self):
        """Setup Reddit API client"""
        try:
            if Config.REDDIT_CLIENT_ID and Config.REDDIT_CLIENT_SECRET:
                self.reddit = praw.Reddit(
                    client_id=Config.REDDIT_CLIENT_ID,
                    client_secret=Config.REDDIT_CLIENT_SECRET,
                    user_agent=Config.REDDIT_USER_AGENT
                )
                logger.info("Reddit client initialized successfully")
            else:
                logger.warning("Reddit API credentials not configured")
        except Exception as e:
            logger.error(f"Failed to initialize Reddit client: {e}")
    
    def search_mentions(self, keywords: List[str], subreddits: List[str] = None, limit: int = 10) -> List[Dict]:
        """
        Search for Reddit posts and comments mentioning keywords
        
        Args:
            keywords: List of keywords to search for
            subreddits: List of subreddit names (if None, searches all)
            limit: Maximum number of results per keyword
        
        Returns:
            List of post/comment data dictionaries
        """
        if not self.reddit:
            logger.warning("Reddit client not initialized")
            return []
        
        results = []
        
        try:
            for keyword in keywords:
                if not keyword.strip():
                    continue
                
                # Search posts
                if subreddits:
                    search_target = '+'.join(subreddits)
                    subreddit = self.reddit.subreddit(search_target)
                else:
                    subreddit = self.reddit.subreddit('all')
                
                posts = subreddit.search(keyword, limit=limit, sort='new')
                
                for post in posts:
                    results.append({
                        'id': post.id,
                        'text': f"{post.title}\n{post.selftext}",
                        'author': str(post.author) if post.author else '[deleted]',
                        'created_at': datetime.fromtimestamp(post.created_utc, tz=timezone.utc).isoformat(),
                        'url': f"https://reddit.com{post.permalink}",
                        'engagement': post.score + post.num_comments,
                        'subreddit': str(post.subreddit)
                    })
            
            logger.info(f"Found {len(results)} Reddit posts")
            return results
            
        except Exception as e:
            logger.error(f"Error searching Reddit: {e}")
            return []
    
    def get_subreddit_posts(self, subreddit_name: str, limit: int = 10) -> List[Dict]:
        """
        Get recent posts from a specific subreddit
        
        Args:
            subreddit_name: Name of the subreddit
            limit: Maximum number of posts
        
        Returns:
            List of post data dictionaries
        """
        if not self.reddit:
            return []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = subreddit.new(limit=limit)
            
            results = []
            for post in posts:
                results.append({
                    'id': post.id,
                    'text': f"{post.title}\n{post.selftext}",
                    'author': str(post.author) if post.author else '[deleted]',
                    'created_at': datetime.fromtimestamp(post.created_utc, tz=timezone.utc).isoformat(),
                    'url': f"https://reddit.com{post.permalink}",
                    'engagement': post.score + post.num_comments,
                    'subreddit': str(post.subreddit)
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting subreddit posts: {e}")
            return []
    
    def monitor_comments(self, subreddit_name: str, keywords: List[str], limit: int = 20) -> List[Dict]:
        """
        Monitor recent comments in a subreddit for keywords
        
        Args:
            subreddit_name: Name of the subreddit
            keywords: Keywords to look for
            limit: Maximum number of comments to check
        
        Returns:
            List of matching comment data
        """
        if not self.reddit:
            return []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            comments = subreddit.comments(limit=limit)
            
            results = []
            keywords_lower = [k.lower() for k in keywords if k.strip()]
            
            for comment in comments:
                comment_text_lower = comment.body.lower()
                
                # Check if any keyword is in the comment
                if any(keyword in comment_text_lower for keyword in keywords_lower):
                    results.append({
                        'id': comment.id,
                        'text': comment.body,
                        'author': str(comment.author) if comment.author else '[deleted]',
                        'created_at': datetime.fromtimestamp(comment.created_utc, tz=timezone.utc).isoformat(),
                        'url': f"https://reddit.com{comment.permalink}",
                        'engagement': comment.score,
                        'subreddit': str(comment.subreddit)
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error monitoring comments: {e}")
            return []

