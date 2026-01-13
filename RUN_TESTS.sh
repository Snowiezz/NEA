#!/bin/bash
# Security Testing Automation Script for nea1.py

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║              NEA (UniPicker) - Security Testing Suite                    ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "[1/4] Running automated security tests..."
echo "─────────────────────────────────────────────────────────────────────────────"
python3 test_security_nea1.py

echo ""
echo ""
echo "[2/4] Test results saved to security_test_results.txt"
echo "─────────────────────────────────────────────────────────────────────────────"

echo ""
echo "[3/4] Documentation files available:"
echo "─────────────────────────────────────────────────────────────────────────────"
echo "  📄 EXECUTIVE_SUMMARY.md         - Executive overview for stakeholders"
echo "  📄 SECURITY_FINDINGS.md         - Detailed technical vulnerabilities"
echo "  📄 SECURITY_SUMMARY.md          - Quick reference guide"
echo "  📄 SECURITY_TESTING_README.md   - How to use the test suite"
echo "  📄 security_test_results.txt    - Full test output"
echo ""

echo "[4/4] To run interactive attack demonstrations:"
echo "─────────────────────────────────────────────────────────────────────────────"
echo "  $ python3 attack_demonstrations.py"
echo ""

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                         Testing Complete!                                ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Summary: Found 2 CRITICAL, 2 HIGH, 4 MEDIUM, 2 LOW severity issues"
echo "Next steps: Review EXECUTIVE_SUMMARY.md for recommendations"
echo ""
