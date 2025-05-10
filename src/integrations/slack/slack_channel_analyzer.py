import os
from typing import List, Dict, Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class SlackChannelAnalyzer:
    def __init__(self, bot_token: str = None):
        """
        Initialize the Slack channel analyzer with a bot token.
        
        Args:
            bot_token (str): The Bot User OAuth Token. If not provided, will try to get from SLACK_BOT_TOKEN env var.
        """
        self.bot_token = bot_token or os.getenv('SLACK_BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("Bot token is required. Please provide it or set SLACK_BOT_TOKEN environment variable.")
        
        if not self.bot_token.startswith('xoxb-'):
            raise ValueError("Invalid bot token format. Bot tokens should start with 'xoxb-'")
            
        self.client = WebClient(token=self.bot_token)
        
    def _validate_token(self) -> bool:
        """
        Validate the bot token by making a test API call.
        
        Returns:
            bool: True if token is valid, False otherwise
        """
        try:
            # Try to get bot info as a simple validation
            response = self.client.auth_test()
            return response["ok"]
        except SlackApiError as e:
            logger.error(f"Token validation failed: {str(e)}")
            return False

    def list_channels(self) -> List[Dict[str, Any]]:
        """
        List all channels the bot has access to.
        
        Returns:
            List[Dict[str, Any]]: List of channels with their details
        """
        if not self._validate_token():
            raise ValueError("Invalid bot token. Please check your token and permissions.")
            
        try:
            result = self.client.conversations_list(
                types="public_channel,private_channel",
                limit=1000
            )
            
            if not result["ok"]:
                raise Exception(f"Failed to list channels: {result.get('error')}")
                
            return result["channels"]
            
        except SlackApiError as e:
            logger.error(f"Error listing channels: {str(e)}")
            raise

    def get_channel_info(self, channel_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific channel.
        
        Args:
            channel_id (str): The ID of the channel to get info for
            
        Returns:
            Dict[str, Any]: Channel information
        """
        if not self._validate_token():
            raise ValueError("Invalid bot token. Please check your token and permissions.")
            
        try:
            result = self.client.conversations_info(channel=channel_id)
            
            if not result["ok"]:
                raise Exception(f"Failed to get channel info: {result.get('error')}")
                
            return result["channel"]
            
        except SlackApiError as e:
            logger.error(f"Error getting channel info: {str(e)}")
            raise
            
    def get_channel_messages(self, channel_id: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get messages from a Slack channel for the specified number of days.
        
        Args:
            channel_id (str): The ID of the channel to analyze
            days (int): Number of days of history to retrieve (default: 7)
            
        Returns:
            List[Dict[str, Any]]: List of messages with their metadata
        """
        if not self._validate_token():
            raise ValueError("Invalid bot token. Please check your token and permissions.")
            
        try:
            # Calculate the timestamp for N days ago
            oldest = (datetime.now() - timedelta(days=days)).timestamp()
            
            # Get channel messages
            result = self.client.conversations_history(
                channel=channel_id,
                oldest=oldest,
                limit=1000  # Adjust as needed
            )
            
            if not result["ok"]:
                raise Exception(f"Failed to get channel messages: {result.get('error')}")
                
            return result["messages"]
            
        except SlackApiError as e:
            logger.error(f"Error getting channel messages: {str(e)}")
            raise
            
    def analyze_channel(self, channel_id: str, days: int = 7) -> Dict[str, Any]:
        """
        Analyze a Slack channel's messages and return insights.
        
        Args:
            channel_id (str): The ID of the channel to analyze
            days (int): Number of days of history to analyze (default: 7)
            
        Returns:
            Dict[str, Any]: Analysis results including message count, user activity, etc.
        """
        if not self._validate_token():
            raise ValueError("Invalid bot token. Please check your token and permissions.")
            
        try:
            messages = self.get_channel_messages(channel_id, days)
            
            # Basic analysis
            analysis = {
                "channel_id": channel_id,
                "total_messages": len(messages),
                "unique_users": len(set(msg.get("user") for msg in messages if msg.get("user"))),
                "message_types": {},
                "user_activity": {},
                "time_distribution": {
                    "morning": 0,  # 6-12
                    "afternoon": 0,  # 12-18
                    "evening": 0,  # 18-24
                    "night": 0,  # 0-6
                }
            }
            
            for msg in messages:
                # Count message types
                msg_type = msg.get("type", "unknown")
                analysis["message_types"][msg_type] = analysis["message_types"].get(msg_type, 0) + 1
                
                # Count user activity
                user = msg.get("user")
                if user:
                    analysis["user_activity"][user] = analysis["user_activity"].get(user, 0) + 1
                
                # Analyze time distribution
                if "ts" in msg:
                    msg_time = datetime.fromtimestamp(float(msg["ts"]))
                    hour = msg_time.hour
                    
                    if 6 <= hour < 12:
                        analysis["time_distribution"]["morning"] += 1
                    elif 12 <= hour < 18:
                        analysis["time_distribution"]["afternoon"] += 1
                    elif 18 <= hour < 24:
                        analysis["time_distribution"]["evening"] += 1
                    else:
                        analysis["time_distribution"]["night"] += 1
            
            return analysis
            
        except SlackApiError as e:
            logger.error(f"Error analyzing channel: {str(e)}")
            raise 