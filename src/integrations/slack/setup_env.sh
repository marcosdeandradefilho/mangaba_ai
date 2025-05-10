#!/bin/bash

# Set Slack environment variables
export SLACK_BOT_TOKEN='YOUR_SLACK_BOT_TOKEN'
export SLACK_WORKSPACE_ID='YOUR_WORKSPACE_ID'
export SLACK_CHANNEL_ID='YOUR_CHANNEL_ID'

# Print confirmation
echo "Environment variables set:"
echo "SLACK_BOT_TOKEN: ${SLACK_BOT_TOKEN:0:10}..."
echo "SLACK_WORKSPACE_ID: $SLACK_WORKSPACE_ID"
echo "SLACK_CHANNEL_ID: $SLACK_CHANNEL_ID"

# Run the analyzer
echo -e "\nRunning Mangaba Channel Analyzer..."
python src/integrations/slack/mangaba_channel_analyzer.py 