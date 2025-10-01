#!/bin/bash

echo "🔍 Security Check - Scanning for sensitive data..."

# Check for hardcoded secrets (exclude example files and documentation)
echo "Checking for hardcoded secrets..."
if grep -r -i --exclude-dir=.git --exclude-dir=.venv --exclude-dir=.terraform \
   --exclude="*.example" --exclude="*.md" --exclude="security-check.sh" \
   -E "(api_key|secret|password|token|credential).*=.*['\"][A-Za-z0-9]{20,}" . 2>/dev/null; then
    echo "❌ Found potential hardcoded secrets!"
    exit 1
fi

# Check for sensitive files in git
echo "Checking for sensitive files in git..."
if git ls-files | grep -E "\.(env|tfstate|json|key|pem)$" | grep -v package; then
    echo "❌ Found sensitive files in git!"
    exit 1
fi

# Check for large files that might contain secrets
echo "Checking for large files..."
find . -type f -size +1M -not -path "./.git/*" -not -path "./.venv/*" -not -path "./.terraform/*"

echo "✅ Security check passed!"
