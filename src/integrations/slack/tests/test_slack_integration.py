import unittest
import os
import sys
from datetime import datetime
from slack_sdk.errors import SlackApiError

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.integrations.slack.mangaba_channel_analyzer import MangabaChannelAnalyzer
from src.integrations.slack.slack_agent_handler import SlackAgentHandler

class TestSlackIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment variables."""
        cls.bot_token = os.getenv('SLACK_BOT_TOKEN', 'YOUR_SLACK_BOT_TOKEN')
        cls.workspace_id = os.getenv('SLACK_WORKSPACE_ID', 'YOUR_WORKSPACE_ID')
        cls.channel_id = os.getenv('SLACK_CHANNEL_ID', 'YOUR_CHANNEL_ID')
        
    def setUp(self):
        """Set up test cases."""
        self.analyzer = MangabaChannelAnalyzer(
            bot_token=self.bot_token,
            workspace_id=self.workspace_id,
            channel_id=self.channel_id
        )
        
    def test_token_validation(self):
        """Test bot token validation."""
        try:
            self.analyzer._validate_token()
        except Exception as e:
            self.fail(f"Token validation failed: {str(e)}")
            
    def test_workspace_id_match(self):
        """Test if workspace ID matches the token."""
        result = self.analyzer.handler.client.auth_test()
        self.assertEqual(
            result.get("team_id"),
            self.workspace_id,
            "Workspace ID doesn't match the token"
        )
        
    def test_channel_access(self):
        """Test if bot has access to the channel."""
        try:
            result = self.analyzer.handler.client.conversations_info(
                channel=self.channel_id
            )
            self.assertTrue(result["ok"], "Failed to access channel")
        except SlackApiError as e:
            self.fail(f"Channel access failed: {str(e)}")
            
    def test_message_analysis(self):
        """Test message analysis functionality."""
        try:
            # Get channel messages
            result = self.analyzer.handler.client.conversations_history(
                channel=self.channel_id,
                limit=10  # Limit to last 10 messages for testing
            )
            
            if not result["ok"]:
                self.fail("Failed to get channel messages")
                
            messages = result["messages"]
            analysis = self.analyzer._analyze_messages(messages)
            
            # Verify analysis structure
            self.assertIn("total_messages", analysis)
            self.assertIn("unique_users", analysis)
            self.assertIn("user_activity", analysis)
            self.assertIn("time_distribution", analysis)
            self.assertIn("topics", analysis)
            
            # Verify topics structure
            topics = analysis["topics"]
            self.assertIn("code", topics)
            self.assertIn("architecture", topics)
            self.assertIn("integration", topics)
            self.assertIn("planning", topics)
            self.assertIn("other", topics)
            
        except Exception as e:
            self.fail(f"Message analysis failed: {str(e)}")
            
    def test_agent_registration(self):
        """Test agent registration and configuration."""
        # Verify agents are registered
        self.assertIn("repo_analyzer", self.analyzer.handler.agents)
        self.assertIn("comm_analyzer", self.analyzer.handler.agents)
        self.assertIn("integration_expert", self.analyzer.handler.agents)
        
        # Verify agent configurations
        repo_agent = self.analyzer.handler.agents["repo_analyzer"]
        self.assertEqual(repo_agent["role"], "Code Analyst")
        self.assertIn("code_analysis", repo_agent["capabilities"])
        
    def test_message_sending(self):
        """Test sending messages through agents."""
        try:
            # Test sending a message
            result = self.analyzer.handler.send_agent_message(
                channel_id=self.channel_id,
                agent_id="repo_analyzer",
                message="Test message from integration test"
            )
            
            self.assertTrue(result["ok"], "Failed to send message")
            
        except Exception as e:
            self.fail(f"Message sending failed: {str(e)}")
            
    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Test invalid channel ID
        with self.assertRaises(SlackApiError):
            self.analyzer.analyze_channel("invalid_channel_id")
            
        # Test invalid token
        with self.assertRaises(ValueError):
            MangabaChannelAnalyzer(bot_token="invalid_token")
            
    def test_time_analysis(self):
        """Test time-based analysis functionality."""
        try:
            # Get channel messages
            result = self.analyzer.handler.client.conversations_history(
                channel=self.channel_id,
                limit=100
            )
            
            if not result["ok"]:
                self.fail("Failed to get channel messages")
                
            messages = result["messages"]
            analysis = self.analyzer._analyze_messages(messages)
            
            # Verify time distribution
            time_dist = analysis["time_distribution"]
            self.assertIsInstance(time_dist, dict)
            
            # Test peak hours calculation
            peak_hours = self.analyzer._get_peak_hours(time_dist)
            self.assertIsInstance(peak_hours, str)
            
        except Exception as e:
            self.fail(f"Time analysis failed: {str(e)}")
            
    def test_user_activity_analysis(self):
        """Test user activity analysis."""
        try:
            # Get channel messages
            result = self.analyzer.handler.client.conversations_history(
                channel=self.channel_id,
                limit=100
            )
            
            if not result["ok"]:
                self.fail("Failed to get channel messages")
                
            messages = result["messages"]
            analysis = self.analyzer._analyze_messages(messages)
            
            # Verify user activity
            user_activity = analysis["user_activity"]
            self.assertIsInstance(user_activity, dict)
            
            # Verify activity counts
            for user, count in user_activity.items():
                self.assertIsInstance(count, int)
                self.assertGreaterEqual(count, 0)
                
        except Exception as e:
            self.fail(f"User activity analysis failed: {str(e)}")

if __name__ == '__main__':
    unittest.main() 