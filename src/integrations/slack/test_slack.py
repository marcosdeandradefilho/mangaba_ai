import os
import sys
import unittest
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.integrations.slack.mangaba_channel_analyzer import MangabaChannelAnalyzer

# Load environment variables
load_dotenv()

class TestSlackIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.bot_token = os.getenv('SLACK_BOT_TOKEN')
        if not self.bot_token:
            self.skipTest("SLACK_BOT_TOKEN environment variable not set")
            
        self.channel_id = os.getenv('SLACK_CHANNEL_ID')
        if not self.channel_id:
            self.skipTest("SLACK_CHANNEL_ID environment variable not set")
            
        self.client = WebClient(token=self.bot_token)
        
    def test_bot_connection(self):
        """Test if bot can connect to Slack."""
        try:
            result = self.client.auth_test()
            self.assertTrue(result["ok"], "Failed to connect to Slack")
            print(f"Connected to workspace: {result['team']}")
        except SlackApiError as e:
            self.fail(f"Connection failed: {str(e)}")
            
    def test_channel_access(self):
        """Test if bot can access the channel."""
        try:
            result = self.client.conversations_info(channel=self.channel_id)
            self.assertTrue(result["ok"], "Failed to access channel")
            print(f"Channel name: {result['channel']['name']}")
        except SlackApiError as e:
            self.fail(f"Channel access failed: {str(e)}")
            
    def test_message_retrieval(self):
        """Test if bot can retrieve messages."""
        try:
            result = self.client.conversations_history(
                channel=self.channel_id,
                limit=5
            )
            self.assertTrue(result["ok"], "Failed to get messages")
            print(f"Retrieved {len(result['messages'])} messages")
        except SlackApiError as e:
            self.fail(f"Message retrieval failed: {str(e)}")
            
    def test_message_sending(self):
        """Test if bot can send messages."""
        try:
            result = self.client.chat_postMessage(
                channel=self.channel_id,
                text="Test message from integration test"
            )
            self.assertTrue(result["ok"], "Failed to send message")
            print("Message sent successfully")
        except SlackApiError as e:
            self.fail(f"Message sending failed: {str(e)}")
            
    def test_analyzer_initialization(self):
        """Test if MangabaChannelAnalyzer can be initialized."""
        try:
            analyzer = MangabaChannelAnalyzer(bot_token=self.bot_token)
            self.assertIsNotNone(analyzer)
            print("Analyzer initialized successfully")
        except Exception as e:
            self.fail(f"Analyzer initialization failed: {str(e)}")

def run_tests():
    """Run all tests and print results."""
    print("\nRunning Slack Integration Tests...")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSlackIntegration)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\nTest Summary:")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\nAll tests passed successfully! 🎉")
    else:
        print("\nSome tests failed. Please check the output above. ❌")
        
    return result.wasSuccessful()

if __name__ == '__main__':
    run_tests() 