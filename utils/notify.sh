#!/bin/bash
set -e

reports_dir="./reports"

api_report="$reports_dir/api/api_test_report.html"
web_report="$reports_dir/web/web_test_report.html"

extract_test_results() {
    local file="$1"
    if [[ -f "$file" ]]; then
        local passed=$(grep -oP '(?<=passed=)[0-9]+' "$file" || echo 0)
        local failed=$(grep -oP '(?<=failed=)[0-9]+' "$file" || echo 0)
        local skipped=$(grep -oP '(?<=skipped=)[0-9]+' "$file" || echo 0)
        echo "$passed $failed $skipped"
    else
        echo "0 0 0"
    fi
}

api_results=$(extract_test_results "$api_report")
web_results=$(extract_test_results "$web_report")

api_passed=$(echo "$api_results" | cut -d' ' -f1)
api_failed=$(echo "$api_results" | cut -d' ' -f2)
api_skipped=$(echo "$api_results" | cut -d' ' -f3)

web_passed=$(echo "$web_results" | cut -d' ' -f1)
web_failed=$(echo "$web_results" | cut -d' ' -f2)
web_skipped=$(echo "$web_results" | cut -d' ' -f3)

status="PASSED"
color="good"
if [[ $api_failed -gt 0 || $web_failed -gt 0 ]]; then
    status="FAILED"
    color="danger"
fi

message="*Crypto QA Framework*\n"
message+="API Tests: ${api_passed} ✅ / ${api_failed} ❌ / ${api_skipped} 🚫\n"
message+="Web Tests: ${web_passed} ✅ / ${web_failed} ❌ / ${web_skipped} 🚫\n"
message+="Status: *${status}*\n"

if [[ -n "$SLACK_WEBHOOK_URL" ]]; then
    curl -X POST -H 'Content-type: application/json' --data "$(jq -n --arg text "$message" '{"text":$text}')" "$SLACK_WEBHOOK_URL"
fi

if [[ -n "$EMAIL_RECIPIENT" ]]; then
    subject="Crypto QA Framework Test Results: $status"
    echo -e "$message" | mail -s "$subject" "$EMAIL_RECIPIENT"
fi

echo "Notification process completed successfully."
