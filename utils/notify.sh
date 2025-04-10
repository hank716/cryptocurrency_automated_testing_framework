#!/bin/bash

# Notification script for test results
# This script sends notifications about test results via email and Slack

# Configure logging
log_file="notify.log"
exec > >(tee -a "$log_file") 2>&1

echo "$(date): Starting notification process..."

# Check if required environment variables are set
if [ -z "$SLACK_WEBHOOK_URL" ]; then
    echo "$(date): Warning: SLACK_WEBHOOK_URL is not set. Slack notifications will be skipped."
fi

if [ -z "$EMAIL_RECIPIENT" ]; then
    echo "$(date): Warning: EMAIL_RECIPIENT is not set. Email notifications will be skipped."
fi

# Find test reports
reports_dir="../reports"
if [ ! -d "$reports_dir" ]; then
    echo "$(date): Error: Reports directory not found: $reports_dir"
    exit 1
fi

# Get the latest report directory
latest_report_dir=$(ls -td "$reports_dir"/*/ | head -1)
if [ -z "$latest_report_dir" ]; then
    echo "$(date): Error: No report directories found in $reports_dir"
    exit 1
fi

echo "$(date): Found latest report directory: $latest_report_dir"

# Count test results
api_report="$latest_report_dir/api_test_report.html"
web_report="$latest_report_dir/web_test_report.html"
performance_reports=("$latest_report_dir/api_load_test_report.html" 
                     "$latest_report_dir/web_load_test_report.html"
                     "$latest_report_dir/stress_test_report.html")

# Function to extract test results from HTML report
extract_test_results() {
    local report_file="$1"
    if [ -f "$report_file" ]; then
        # Extract test counts using grep and sed
        local passed=$(grep -o "passed=[0-9]*" "$report_file" | sed 's/passed=//')
        local failed=$(grep -o "failed=[0-9]*" "$report_file" | sed 's/failed=//')
        local skipped=$(grep -o "skipped=[0-9]*" "$report_file" | sed 's/skipped=//')
        
        echo "$passed $failed $skipped"
    else
        echo "0 0 0"
    fi
}

# Get test results
api_results=$(extract_test_results "$api_report")
web_results=$(extract_test_results "$web_report")

api_passed=$(echo "$api_results" | cut -d' ' -f1)
api_failed=$(echo "$api_results" | cut -d' ' -f2)
api_skipped=$(echo "$api_results" | cut -d' ' -f3)

web_passed=$(echo "$web_results" | cut -d' ' -f1)
web_failed=$(echo "$web_results" | cut -d' ' -f2)
web_skipped=$(echo "$web_results" | cut -d' ' -f3)

# Determine overall status
if [ "$api_failed" -gt 0 ] || [ "$web_failed" -gt 0 ]; then
    status="FAILED"
    color="danger"
else
    status="PASSED"
    color="good"
fi

# Create notification message
message="Test Results: $status\n\n"
message+="API Tests: $api_passed passed, $api_failed failed, $api_skipped skipped\n"
message+="Web Tests: $web_passed passed, $web_failed failed, $web_skipped skipped\n\n"
message+="Performance Tests: Completed\n\n"
message+="Report Directory: $latest_report_dir"

echo "$(date): Notification message:"
echo -e "$message"

# Send Slack notification
if [ -n "$SLACK_WEBHOOK_URL" ]; then
    echo "$(date): Sending Slack notification..."
    
    # Create JSON payload
    json_payload=$(cat <<EOF
{
    "attachments": [
        {
            "fallback": "Test Results: $status",
            "color": "$color",
            "title": "Test Results: $status",
            "text": "$(echo -e "$message" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | sed 's/\n/\\n/g')",
            "fields": [
                {
                    "title": "API Tests",
                    "value": "$api_passed passed, $api_failed failed, $api_skipped skipped",
                    "short": true
                },
                {
                    "title": "Web Tests",
                    "value": "$web_passed passed, $web_failed failed, $web_skipped skipped",
                    "short": true
                }
            ],
            "footer": "Crypto QA Framework",
            "ts": $(date +%s)
        }
    ]
}
EOF
)
    
    # Send to Slack
    curl -s -X POST -H "Content-type: application/json" --data "$json_payload" "$SLACK_WEBHOOK_URL"
    
    echo "$(date): Slack notification sent."
fi

# Send email notification
if [ -n "$EMAIL_RECIPIENT" ]; then
    echo "$(date): Sending email notification..."
    
    # Create email subject
    subject="Crypto QA Framework - Test Results: $status"
    
    # Send email
    echo -e "$message" | mail -s "$subject" "$EMAIL_RECIPIENT"
    
    echo "$(date): Email notification sent to $EMAIL_RECIPIENT."
fi

echo "$(date): Notification process completed."
exit 0
