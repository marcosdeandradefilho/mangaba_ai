import os
from typing import Dict, Any, List, Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime, timedelta
import logging
import json
from collections import defaultdict

logger = logging.getLogger(__name__)

class SlackAgentHandler:
    def __init__(self, bot_token: str = None):
        """
        Initialize the Slack agent handler with a bot token.
        
        Args:
            bot_token (str): The Bot User OAuth Token. If not provided, will try to get from SLACK_BOT_TOKEN env var.
        """
        self.bot_token = bot_token or os.getenv('SLACK_BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("Bot token is required. Please provide it or set SLACK_BOT_TOKEN environment variable.")
        
        if not self.bot_token.startswith('xoxb-'):
            raise ValueError("Invalid bot token format. Bot tokens should start with 'xoxb-'")
            
        self.client = WebClient(token=self.bot_token)
        self.agents = {}  # Store agent configurations
        self.conversation_history = defaultdict(list)  # Store conversation history by channel
        
    def register_agent(self, agent_id: str, agent_config: Dict[str, Any]) -> None:
        """
        Register an agent with its configuration.
        
        Args:
            agent_id (str): Unique identifier for the agent
            agent_config (Dict[str, Any]): Agent configuration including name, role, and capabilities
        """
        self.agents[agent_id] = {
            "id": agent_id,
            "name": agent_config.get("name", f"Agent {agent_id}"),
            "role": agent_config.get("role", "assistant"),
            "capabilities": agent_config.get("capabilities", []),
            "active": True,
            "personality": agent_config.get("personality", "professional")
        }
        
    def send_agent_message(self, channel_id: str, agent_id: str, message: str, 
                          thread_ts: Optional[str] = None, blocks: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Send a message to a channel as a specific agent.
        
        Args:
            channel_id (str): The channel to send the message to
            agent_id (str): The ID of the agent sending the message
            message (str): The message content
            thread_ts (Optional[str]): Thread timestamp if replying to a thread
            blocks (Optional[List[Dict]]): Custom message blocks for rich formatting
            
        Returns:
            Dict[str, Any]: The response from Slack API
        """
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not registered")
            
        agent = self.agents[agent_id]
        
        # Create a rich message with agent information
        if blocks is None:
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{agent['name']}* ({agent['role']})\n{message}"
                    }
                }
            ]
        
        try:
            result = self.client.chat_postMessage(
                channel=channel_id,
                blocks=blocks,
                thread_ts=thread_ts
            )
            
            # Store the message in conversation history
            self.conversation_history[channel_id].append({
                "agent_id": agent_id,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "thread_ts": thread_ts
            })
            
            return result
        except SlackApiError as e:
            logger.error(f"Error sending message: {str(e)}")
            raise
            
    def handle_message(self, event: Dict[str, Any]) -> None:
        """
        Handle incoming messages and route them to appropriate agents.
        
        Args:
            event (Dict[str, Any]): The Slack event data
        """
        if event.get("type") != "message" or event.get("subtype") == "bot_message":
            return
            
        message = event.get("text", "")
        channel_id = event.get("channel")
        thread_ts = event.get("thread_ts") or event.get("ts")
        user_id = event.get("user")
        
        # Store user message in conversation history
        self.conversation_history[channel_id].append({
            "user_id": user_id,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "thread_ts": thread_ts
        })
        
        # Enhanced message routing based on content
        message_lower = message.lower()
        
        if "analyze" in message_lower or "insights" in message_lower:
            self._handle_analysis_request(channel_id, message, thread_ts, user_id)
        elif "help" in message_lower or "what can you do" in message_lower:
            self._handle_help_request(channel_id, thread_ts)
        elif "summary" in message_lower or "overview" in message_lower:
            self._handle_summary_request(channel_id, thread_ts)
        elif "trends" in message_lower or "patterns" in message_lower:
            self._handle_trends_request(channel_id, thread_ts)
            
    def _handle_analysis_request(self, channel_id: str, message: str, thread_ts: str, user_id: str) -> None:
        """Handle requests for analysis with enhanced insights."""
        try:
            # Initial response
            self.send_agent_message(
                channel_id=channel_id,
                agent_id="analyzer",
                message="I'll analyze the channel content for you. Please give me a moment...",
                thread_ts=thread_ts
            )
            
            # Get channel messages
            result = self.client.conversations_history(
                channel=channel_id,
                limit=1000
            )
            
            if not result["ok"]:
                raise Exception(f"Failed to get channel messages: {result.get('error')}")
                
            messages = result["messages"]
            
            # Enhanced analysis
            analysis = self._analyze_messages(messages)
            
            # Create rich message blocks
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Channel Analysis Report*\n\n"
                               f"• Total Messages: {analysis['total_messages']}\n"
                               f"• Unique Users: {analysis['unique_users']}\n"
                               f"• Most Active Time: {analysis['most_active_time']}\n"
                               f"• Conversation Topics: {', '.join(analysis['top_topics'][:3])}"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*User Activity*\n" + "\n".join(
                            f"• <@{user}>: {count} messages"
                            for user, count in analysis['user_activity'].items()
                        )
                    }
                }
            ]
            
            self.send_agent_message(
                channel_id=channel_id,
                agent_id="analyzer",
                message="Analysis complete! Here are the insights:",
                thread_ts=thread_ts,
                blocks=blocks
            )
            
        except Exception as e:
            logger.error(f"Error handling analysis request: {str(e)}")
            self.send_agent_message(
                channel_id=channel_id,
                agent_id="analyzer",
                message="I encountered an error while analyzing the channel. Please try again later.",
                thread_ts=thread_ts
            )
            
    def _analyze_messages(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze messages to extract insights."""
        analysis = {
            "total_messages": len(messages),
            "unique_users": len(set(msg.get("user") for msg in messages if msg.get("user"))),
            "user_activity": defaultdict(int),
            "time_distribution": defaultdict(int),
            "top_topics": [],
            "most_active_time": ""
        }
        
        # Analyze messages
        for msg in messages:
            # User activity
            user = msg.get("user")
            if user:
                analysis["user_activity"][user] += 1
            
            # Time distribution
            if "ts" in msg:
                msg_time = datetime.fromtimestamp(float(msg["ts"]))
                hour = msg_time.hour
                analysis["time_distribution"][hour] += 1
        
        # Find most active time
        if analysis["time_distribution"]:
            most_active_hour = max(analysis["time_distribution"].items(), key=lambda x: x[1])[0]
            analysis["most_active_time"] = f"{most_active_hour:02d}:00"
        
        # Sort user activity
        analysis["user_activity"] = dict(sorted(
            analysis["user_activity"].items(),
            key=lambda x: x[1],
            reverse=True
        ))
        
        return analysis
            
    def _handle_help_request(self, channel_id: str, thread_ts: str) -> None:
        """Handle help requests with enhanced capabilities."""
        try:
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Available Commands*\n\n"
                               "• `analyze` - Get channel insights and statistics\n"
                               "• `summary` - Get a summary of recent discussions\n"
                               "• `trends` - Identify patterns and trends\n"
                               "• `help` - Show this help message"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Active Agents*\n" + "\n".join(
                            f"• *{agent['name']}* ({agent['role']})"
                            for agent in self.agents.values()
                            if agent["active"]
                        )
                    }
                }
            ]
            
            self.send_agent_message(
                channel_id=channel_id,
                agent_id="helper",
                message="Here's what I can help you with:",
                thread_ts=thread_ts,
                blocks=blocks
            )
        except Exception as e:
            logger.error(f"Error handling help request: {str(e)}")
            
    def _handle_summary_request(self, channel_id: str, thread_ts: str) -> None:
        """Handle requests for conversation summary."""
        try:
            # Get recent messages
            result = self.client.conversations_history(
                channel=channel_id,
                limit=50  # Last 50 messages
            )
            
            if not result["ok"]:
                raise Exception(f"Failed to get channel messages: {result.get('error')}")
                
            messages = result["messages"]
            
            # Create summary
            summary = self._create_summary(messages)
            
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Recent Channel Summary*\n\n{summary}"
                    }
                }
            ]
            
            self.send_agent_message(
                channel_id=channel_id,
                agent_id="researcher",
                message="Here's a summary of recent discussions:",
                thread_ts=thread_ts,
                blocks=blocks
            )
        except Exception as e:
            logger.error(f"Error handling summary request: {str(e)}")
            
    def _create_summary(self, messages: List[Dict[str, Any]]) -> str:
        """Create a summary of recent messages."""
        if not messages:
            return "No recent messages to summarize."
            
        # Group messages by user
        user_messages = defaultdict(list)
        for msg in messages:
            user = msg.get("user", "unknown")
            text = msg.get("text", "")
            if text:
                user_messages[user].append(text)
        
        # Create summary
        summary_parts = []
        for user, msgs in user_messages.items():
            summary_parts.append(f"• <@{user}> contributed {len(msgs)} messages")
        
        return "\n".join(summary_parts)
            
    def _handle_trends_request(self, channel_id: str, thread_ts: str) -> None:
        """Handle requests for trend analysis."""
        try:
            # Get channel messages
            result = self.client.conversations_history(
                channel=channel_id,
                limit=1000
            )
            
            if not result["ok"]:
                raise Exception(f"Failed to get channel messages: {result.get('error')}")
                
            messages = result["messages"]
            
            # Analyze trends
            trends = self._analyze_trends(messages)
            
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Channel Trends Analysis*\n\n{trends}"
                    }
                }
            ]
            
            self.send_agent_message(
                channel_id=channel_id,
                agent_id="researcher",
                message="Here are the trends I've identified:",
                thread_ts=thread_ts,
                blocks=blocks
            )
        except Exception as e:
            logger.error(f"Error handling trends request: {str(e)}")
            
    def _analyze_trends(self, messages: List[Dict[str, Any]]) -> str:
        """Analyze message trends."""
        if not messages:
            return "No messages to analyze for trends."
            
        # Basic trend analysis
        time_distribution = defaultdict(int)
        for msg in messages:
            if "ts" in msg:
                msg_time = datetime.fromtimestamp(float(msg["ts"]))
                hour = msg_time.hour
                time_distribution[hour] += 1
        
        # Find peak activity times
        peak_hours = sorted(time_distribution.items(), key=lambda x: x[1], reverse=True)[:3]
        peak_times = [f"{hour:02d}:00" for hour, _ in peak_hours]
        
        return (
            f"• Peak activity times: {', '.join(peak_times)}\n"
            f"• Total messages analyzed: {len(messages)}\n"
            f"• Time span: {self._get_time_span(messages)}"
        )
        
    def _get_time_span(self, messages: List[Dict[str, Any]]) -> str:
        """Calculate the time span of messages."""
        if not messages:
            return "No messages"
            
        timestamps = [float(msg["ts"]) for msg in messages if "ts" in msg]
        if not timestamps:
            return "Unknown"
            
        oldest = datetime.fromtimestamp(min(timestamps))
        newest = datetime.fromtimestamp(max(timestamps))
        delta = newest - oldest
        
        if delta.days > 0:
            return f"{delta.days} days"
        elif delta.seconds > 3600:
            return f"{delta.seconds // 3600} hours"
        else:
            return f"{delta.seconds // 60} minutes"
            
    def get_agent_status(self) -> List[Dict[str, Any]]:
        """
        Get the status of all registered agents.
        
        Returns:
            List[Dict[str, Any]]: List of agent statuses
        """
        return [
            {
                "id": agent["id"],
                "name": agent["name"],
                "role": agent["role"],
                "active": agent["active"],
                "capabilities": agent["capabilities"],
                "personality": agent["personality"]
            }
            for agent in self.agents.values()
        ] 