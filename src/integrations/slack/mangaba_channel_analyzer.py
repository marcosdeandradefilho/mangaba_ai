from slack_agent_handler import SlackAgentHandler
import logging
import time
from datetime import datetime, timedelta
import os
from typing import Dict, Any, List
from slack_sdk.errors import SlackApiError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default bot token - can be overridden by environment variable
DEFAULT_BOT_TOKEN = "YOUR_SLACK_BOT_TOKEN"

# Slack workspace and channel configuration
WORKSPACE_ID = "T013NTSNZSP"
CHANNEL_ID = "C01N7HUJ6U9"

class MangabaChannelAnalyzer:
    def __init__(self, bot_token: str = None, workspace_id: str = None, channel_id: str = None):
        """
        Initialize the Mangaba Channel Analyzer.
        
        Args:
            bot_token (str, optional): Slack bot token. If not provided, will try to get from SLACK_BOT_TOKEN env var.
            workspace_id (str, optional): Slack workspace ID. If not provided, will use default.
            channel_id (str, optional): Slack channel ID. If not provided, will use default.
        """
        self.bot_token = bot_token or os.getenv('SLACK_BOT_TOKEN', DEFAULT_BOT_TOKEN)
        self.workspace_id = workspace_id or WORKSPACE_ID
        self.channel_id = channel_id or CHANNEL_ID
        
        if not self.bot_token:
            raise ValueError("Bot token is required. Please provide it or set SLACK_BOT_TOKEN environment variable.")
            
        if not self.bot_token.startswith('xoxb-'):
            raise ValueError("Invalid bot token format. Bot tokens should start with 'xoxb-'")
            
        self.handler = SlackAgentHandler(bot_token=self.bot_token)
        self._setup_agents()
        self._validate_token()
        
    def _validate_token(self):
        """Validate the bot token and required scopes."""
        try:
            # Test the token with a simple API call
            result = self.handler.client.auth_test()
            if not result["ok"]:
                raise ValueError(f"Invalid token: {result.get('error')}")
                
            # Verify workspace ID
            if result.get("team_id") != self.workspace_id:
                logger.warning(
                    f"Token workspace ID ({result.get('team_id')}) doesn't match expected workspace ID ({self.workspace_id})"
                )
                
            # Check if we have the required scopes
            scopes = result.get("scopes", [])
            required_scopes = ["chat:write", "channels:history", "groups:history"]
            missing_scopes = [scope for scope in required_scopes if scope not in scopes]
            
            if missing_scopes:
                logger.warning(
                    "Missing required scopes: %s\n"
                    "Please update your Slack app's OAuth scopes and reinstall the app.",
                    ", ".join(missing_scopes)
                )
                
        except SlackApiError as e:
            if e.response["error"] == "missing_scope":
                logger.error(
                    "Missing required scope: %s\n"
                    "Please update your Slack app's OAuth scopes and reinstall the app.",
                    e.response.get("needed")
                )
            raise
        
    def _setup_agents(self):
        """Setup specialized agents for Mangaba analysis."""
        # Repository Analysis Agent
        self.handler.register_agent("repo_analyzer", {
            "name": "Mangaba Repository Analyzer",
            "role": "Code Analyst",
            "capabilities": ["code_analysis", "architecture_review", "dependency_check"],
            "personality": "technical"
        })
        
        # Communication Analysis Agent
        self.handler.register_agent("comm_analyzer", {
            "name": "Communication Analyst",
            "role": "Communication Expert",
            "capabilities": ["message_analysis", "topic_tracking", "engagement_metrics"],
            "personality": "analytical"
        })
        
        # Integration Agent
        self.handler.register_agent("integration_expert", {
            "name": "Integration Specialist",
            "role": "Integration Expert",
            "capabilities": ["slack_integration", "api_analysis", "system_connectivity"],
            "personality": "systematic"
        })
        
    def analyze_channel(self, channel_id: str):
        """Perform comprehensive analysis of the Slack channel."""
        try:
            # Initial message
            self.handler.send_agent_message(
                channel_id=channel_id,
                agent_id="repo_analyzer",
                message="Starting comprehensive analysis of the Mangaba project channel..."
            )
            
            # Get channel messages
            result = self.handler.client.conversations_history(
                channel=channel_id,
                limit=1000
            )
            
            if not result["ok"]:
                raise Exception(f"Failed to get channel messages: {result.get('error')}")
                
            messages = result["messages"]
            
            # Analyze messages
            analysis = self._analyze_messages(messages)
            
            # Send analysis results
            self._send_analysis_results(channel_id, analysis)
            
        except SlackApiError as e:
            error_message = str(e)
            if e.response["error"] == "missing_scope":
                error_message = (
                    f"Missing required scope: {e.response.get('needed')}\n"
                    "Please update your Slack app's OAuth scopes and reinstall the app."
                )
            elif e.response["error"] == "channel_not_found":
                error_message = f"Channel {channel_id} not found. Please check the channel ID."
            elif e.response["error"] == "not_in_channel":
                error_message = f"Bot is not in channel {channel_id}. Please invite the bot to the channel."
                
            logger.error(f"Error during channel analysis: {error_message}")
            raise
            
        except Exception as e:
            logger.error(f"Error during channel analysis: {str(e)}")
            raise
            
    def _analyze_messages(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze messages for Mangaba-specific insights."""
        analysis = {
            "total_messages": len(messages),
            "unique_users": len(set(msg.get("user") for msg in messages if msg.get("user"))),
            "user_activity": {},
            "time_distribution": {},
            "topics": {
                "code": 0,
                "architecture": 0,
                "integration": 0,
                "planning": 0,
                "other": 0
            },
            "key_discussions": []
        }
        
        # Analyze each message
        for msg in messages:
            text = msg.get("text", "").lower()
            user = msg.get("user")
            timestamp = msg.get("ts")
            
            # Track user activity
            if user:
                analysis["user_activity"][user] = analysis["user_activity"].get(user, 0) + 1
            
            # Track time distribution
            if timestamp:
                msg_time = datetime.fromtimestamp(float(timestamp))
                hour = msg_time.hour
                analysis["time_distribution"][hour] = analysis["time_distribution"].get(hour, 0) + 1
            
            # Categorize topics
            if any(word in text for word in ["code", "function", "class", "method"]):
                analysis["topics"]["code"] += 1
            elif any(word in text for word in ["architecture", "design", "structure"]):
                analysis["topics"]["architecture"] += 1
            elif any(word in text for word in ["integration", "api", "connect"]):
                analysis["topics"]["integration"] += 1
            elif any(word in text for word in ["plan", "roadmap", "sprint"]):
                analysis["topics"]["planning"] += 1
            else:
                analysis["topics"]["other"] += 1
            
            # Track key discussions
            if len(text.split()) > 10:  # Consider longer messages as potential key discussions
                analysis["key_discussions"].append({
                    "text": text[:100] + "...",  # Truncate long messages
                    "user": user,
                    "timestamp": timestamp
                })
        
        return analysis
        
    def _send_analysis_results(self, channel_id: str, analysis: Dict[str, Any]):
        """Send formatted analysis results to the channel."""
        # Repository Analysis
        self.handler.send_agent_message(
            channel_id=channel_id,
            agent_id="repo_analyzer",
            message="*Repository Analysis*\n\n" +
                   f"• Total Messages: {analysis['total_messages']}\n" +
                   f"• Unique Contributors: {analysis['unique_users']}\n" +
                   f"• Most Active Time: {self._get_peak_hours(analysis['time_distribution'])}"
        )
        
        # Communication Analysis
        comm_blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Communication Analysis*\n\n" +
                            "*Topic Distribution:*\n" +
                            f"• Code Discussions: {analysis['topics']['code']}\n" +
                            f"• Architecture: {analysis['topics']['architecture']}\n" +
                            f"• Integration: {analysis['topics']['integration']}\n" +
                            f"• Planning: {analysis['topics']['planning']}\n" +
                            f"• Other: {analysis['topics']['other']}"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Top Contributors:*\n" +
                            "\n".join(
                                f"• <@{user}>: {count} messages"
                                for user, count in sorted(
                                    analysis["user_activity"].items(),
                                    key=lambda x: x[1],
                                    reverse=True
                                )[:5]
                            )
                }
            }
        ]
        
        self.handler.send_agent_message(
            channel_id=channel_id,
            agent_id="comm_analyzer",
            message="Here's the communication analysis:",
            blocks=comm_blocks
        )
        
        # Integration Analysis
        if analysis["topics"]["integration"] > 0:
            self.handler.send_agent_message(
                channel_id=channel_id,
                agent_id="integration_expert",
                message="*Integration Insights*\n\n" +
                       "I've noticed significant discussion about integrations. " +
                       "Would you like me to analyze specific integration patterns or " +
                       "provide recommendations for improvement?"
            )
        
    def _get_peak_hours(self, time_distribution: Dict[int, int]) -> str:
        """Get the peak activity hours from time distribution."""
        if not time_distribution:
            return "No activity data"
            
        peak_hours = sorted(time_distribution.items(), key=lambda x: x[1], reverse=True)[:3]
        return ", ".join(f"{hour:02d}:00" for hour, _ in peak_hours)

def main():
    try:
        # Initialize analyzer with token from environment or default
        analyzer = MangabaChannelAnalyzer()
        
        # Perform analysis on the specified channel
        analyzer.analyze_channel(analyzer.channel_id)
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        print("\nTo fix this error, please ensure:")
        print("1. The bot has been added to the channel")
        print("2. The bot has the following OAuth scopes:")
        print("   - channels:history")
        print("   - chat:write")
        print("   - groups:history")
        print("3. The channel ID is correct")
        print("\nTo update scopes:")
        print("1. Go to https://api.slack.com/apps")
        print("2. Select your app")
        print("3. Click 'OAuth & Permissions'")
        print("4. Add the required scopes")
        print("5. Reinstall the app to your workspace")
        print("\nYou can also set the bot token using the SLACK_BOT_TOKEN environment variable:")
        print("export SLACK_BOT_TOKEN='your-bot-token'")
        print("\nCurrent configuration:")
        print(f"Workspace ID: {WORKSPACE_ID}")
        print(f"Channel ID: {CHANNEL_ID}")

if __name__ == "__main__":
    main() 