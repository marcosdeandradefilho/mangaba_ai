# Set Slack environment variables
$env:SLACK_BOT_TOKEN = 'YOUR_SLACK_BOT_TOKEN'
$env:SLACK_WORKSPACE_ID = 'YOUR_WORKSPACE_ID'
$env:SLACK_CHANNEL_ID = 'YOUR_CHANNEL_ID'

# Print confirmation
Write-Host "Environment variables set:"
Write-Host "SLACK_BOT_TOKEN: $($env:SLACK_BOT_TOKEN.Substring(0,10))..."
Write-Host "SLACK_WORKSPACE_ID: $env:SLACK_WORKSPACE_ID"
Write-Host "SLACK_CHANNEL_ID: $env:SLACK_CHANNEL_ID"

# Run the analyzer
Write-Host "`nRunning Mangaba Channel Analyzer..."
python src/integrations/slack/mangaba_channel_analyzer.py 