# Set up environment variables for testing
$env:SLACK_BOT_TOKEN = 'YOUR_SLACK_BOT_TOKEN'
$env:SLACK_WORKSPACE_ID = 'YOUR_WORKSPACE_ID'
$env:SLACK_CHANNEL_ID = 'YOUR_CHANNEL_ID'

# Add the project root to PYTHONPATH
$env:PYTHONPATH = "$PSScriptRoot\..\..\..;$env:PYTHONPATH"

# Run the tests
Write-Host "Running Slack Integration Tests..."
python -m unittest discover -s . -p "test_*.py" -v

# Check if tests passed
if ($LASTEXITCODE -eq 0) {
    Write-Host "`nAll tests passed successfully!" -ForegroundColor Green
} else {
    Write-Host "`nSome tests failed. Please check the output above." -ForegroundColor Red
} 