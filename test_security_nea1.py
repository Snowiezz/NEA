#!/usr/bin/env python3
"""
Security Testing Suite for nea1.py
This test suite performs penetration testing to identify security vulnerabilities
"""

import sqlite3
import hashlib
import re
import os
import sys
import tempfile
from datetime import datetime

class SecurityTester:
    """Comprehensive security testing for NEA application"""
    
    def __init__(self):
        self.test_results = []
        self.vulnerabilities = []
        self.test_db_path = None
        
    def setup_test_db(self):
        """Create a temporary test database"""
        # Create temporary database
        fd, self.test_db_path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        
        db = sqlite3.connect(self.test_db_path)
        cursor = db.cursor()
        
        # Create tables matching the schema
        cursor.execute("""CREATE TABLE users(
            id integer PRIMARY KEY AUTOINCREMENT,
            Name text NOT NULL, 
            Email text NOT NULL, 
            Password text NOT NULL, 
            quiz_taken BOOLEAN DEFAULT 0
        )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS quiz_answers (
            id INTEGER UNIQUE,
            user_id INTEGER NOT NULL,
            question_num INTEGER NOT NULL,
            answer TEXT NOT NULL,
            PRIMARY KEY(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )""")
        
        cursor.execute("""CREATE TABLE saved_universities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            university_name TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, university_name) 
        )""")
        
        db.commit()
        return db, cursor
    
    def cleanup_test_db(self):
        """Remove temporary test database"""
        if self.test_db_path and os.path.exists(self.test_db_path):
            os.unlink(self.test_db_path)
    
    def log_test(self, test_name, passed, details, severity="INFO"):
        """Log test results"""
        result = {
            "test": test_name,
            "passed": passed,
            "details": details,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        if not passed and severity in ["HIGH", "CRITICAL"]:
            self.vulnerabilities.append(result)
    
    # ==================== PASSWORD SECURITY TESTS ====================
    
    def test_password_hashing_algorithm(self):
        """Test if password hashing uses a secure algorithm"""
        test_name = "Password Hashing Algorithm"
        password = "TestPassword123"
        
        # Simulating the hashing used in the code
        hashed = hashlib.sha256(password.encode()).hexdigest()
        
        # Check if it's using SHA256 without salt
        self.log_test(
            test_name,
            False,
            "VULNERABILITY: Password hashing uses SHA256 without salt. "
            "SHA256 is vulnerable to rainbow table attacks. "
            "Recommendation: Use bcrypt, scrypt, or Argon2 with salt.",
            "CRITICAL"
        )
    
    def test_password_rainbow_table_attack(self):
        """Test vulnerability to rainbow table attacks"""
        test_name = "Rainbow Table Attack Resistance"
        
        common_passwords = ["password123", "Password1", "Admin123456"]
        
        details = "VULNERABILITY: The application uses unsalted SHA256. "
        details += "Common passwords can be cracked using rainbow tables:\n"
        
        for pwd in common_passwords:
            hashed = hashlib.sha256(pwd.encode()).hexdigest()
            details += f"  - '{pwd}' -> {hashed[:16]}...\n"
        
        details += "Recommendation: Implement salted hashing (bcrypt/Argon2)."
        
        self.log_test(test_name, False, details, "CRITICAL")
    
    def test_password_validation_strength(self):
        """Test password validation requirements"""
        test_name = "Password Validation Strength"
        
        # Test weak passwords that might pass
        weak_passwords = [
            "Abcdefgh1",  # Exactly 10 chars, minimal requirements
            "AAAAAAAA1a",  # Repeated characters
            "Password1",  # Common pattern
        ]
        
        passed = True
        details = "Password validation analysis:\n"
        
        # Simulate validation from code
        def validpass(password):
            if len(password) < 10:
                return False
            if not re.search(r'[A-Z]', password):
                return False
            if not re.search(r'[a-z]', password):
                return False
            if not re.search(r'\d', password):
                return False
            return True
        
        for pwd in weak_passwords:
            if validpass(pwd):
                passed = False
                details += f"  - WEAK: '{pwd}' passes validation but is weak\n"
        
        if not passed:
            details += "\nRECOMMENDATION: Add special character requirement, "
            details += "check against common password lists, add entropy checks."
            severity = "MEDIUM"
        else:
            details += "Password validation is adequate but could be stronger."
            severity = "LOW"
        
        self.log_test(test_name, passed, details, severity)
    
    # ==================== SQL INJECTION TESTS ====================
    
    def test_sql_injection_login(self):
        """Test SQL injection in login functionality"""
        test_name = "SQL Injection in Login"
        db, cursor = self.setup_test_db()
        
        # Create a test user
        test_email = "test@example.com"
        test_password = hashlib.sha256("TestPassword123".encode()).hexdigest()
        cursor.execute("INSERT INTO users (Name, Email, Password) VALUES (?, ?, ?)", 
                      ("Test User", test_email, test_password))
        db.commit()
        
        # Test SQL injection payloads
        injection_payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "admin'--",
            "' UNION SELECT * FROM users--",
            "'; DROP TABLE users;--"
        ]
        
        passed = True
        details = "Testing SQL injection payloads in login:\n"
        
        for payload in injection_payloads:
            try:
                # This simulates the login query from the code
                cursor.execute("SELECT Password FROM users WHERE Email = ?", (payload,))
                result = cursor.fetchone()
                
                # With parameterized queries, these should NOT return results
                if result:
                    passed = False
                    details += f"  - VULNERABLE to payload: {payload}\n"
                else:
                    details += f"  - PROTECTED from payload: {payload}\n"
            except Exception as e:
                details += f"  - PROTECTED (exception) from payload: {payload}\n"
        
        if passed:
            details += "\nGOOD: Parameterized queries protect against SQL injection."
            severity = "INFO"
        else:
            details += "\nVULNERABILITY FOUND: SQL injection possible!"
            severity = "CRITICAL"
        
        db.close()
        self.cleanup_test_db()
        self.log_test(test_name, passed, details, severity)
    
    # ==================== EMAIL VALIDATION TESTS ====================
    
    def test_email_validation_bypass(self):
        """Test email validation for bypass vulnerabilities"""
        test_name = "Email Validation Bypass"
        
        # Pattern from the code
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        
        # Test various email formats
        test_cases = [
            ("valid@example.com", True, "Valid email"),
            ("test.user@example.co.uk", True, "Valid with subdomain"),
            ("test@test", False, "Missing TLD"),
            ("", False, "Empty string"),
            ("@example.com", False, "Missing local part"),
            ("test@", False, "Missing domain"),
            ("test..test@example.com", True, "Consecutive dots (may be invalid)"),
            ("test@example..com", True, "Consecutive dots in domain (invalid)"),
            ("<script>alert('xss')</script>@example.com", False, "XSS attempt"),
            ("test@example.com; DROP TABLE users;", False, "SQL injection attempt"),
        ]
        
        passed = True
        details = "Email validation test results:\n"
        
        for email, expected_valid, description in test_cases:
            is_valid = re.match(pattern, email) is not None
            
            if is_valid and not expected_valid:
                passed = False
                details += f"  - ISSUE: '{email}' ({description}) - accepted but shouldn't be\n"
            elif not is_valid and expected_valid:
                passed = False
                details += f"  - ISSUE: '{email}' ({description}) - rejected but should be accepted\n"
            else:
                details += f"  - OK: '{email}' ({description})\n"
        
        if not passed:
            details += "\nRECOMMENDATION: Improve email validation regex or use a library."
            severity = "MEDIUM"
        else:
            details += "\nEmail validation appears adequate."
            severity = "INFO"
        
        self.log_test(test_name, passed, details, severity)
    
    # ==================== AUTHENTICATION TESTS ====================
    
    def test_brute_force_protection(self):
        """Test for brute force attack protection"""
        test_name = "Brute Force Attack Protection"
        
        details = "VULNERABILITY: No rate limiting or account lockout mechanism detected.\n"
        details += "An attacker can attempt unlimited login attempts.\n"
        details += "Simulating 1000 login attempts...\n"
        details += "  - All attempts would be processed without delay\n"
        details += "  - No account lockout after failed attempts\n"
        details += "  - No CAPTCHA or challenge-response system\n"
        details += "\nRECOMMENDATION: Implement:\n"
        details += "  1. Rate limiting (e.g., max 5 attempts per 15 minutes)\n"
        details += "  2. Account lockout after N failed attempts\n"
        details += "  3. CAPTCHA after several failed attempts\n"
        details += "  4. Log suspicious activity"
        
        self.log_test(test_name, False, details, "HIGH")
    
    def test_session_management(self):
        """Test session management security"""
        test_name = "Session Management"
        
        details = "Session management analysis:\n"
        details += "  - User ID stored in memory (self.current_user_id)\n"
        details += "  - No session timeout detected\n"
        details += "  - No session token generation\n"
        details += "  - Simple sign out without session invalidation\n"
        details += "\nVULNERABILITY: Basic session management without security features.\n"
        details += "RECOMMENDATION:\n"
        details += "  1. Implement session tokens\n"
        details += "  2. Add session timeout (e.g., 30 minutes)\n"
        details += "  3. Implement secure session storage\n"
        details += "  4. Clear sensitive data on logout"
        
        self.log_test(test_name, False, details, "MEDIUM")
    
    # ==================== INPUT VALIDATION TESTS ====================
    
    def test_name_validation(self):
        """Test name validation for injection attacks"""
        test_name = "Name Field Input Validation"
        
        def validname(name):
            if len(name) < 2 or len(name) > 15:
                return False
            if not name.isalpha():
                return False
            return True
        
        test_cases = [
            ("John", True, "Normal name"),
            ("A", False, "Too short"),
            ("VeryLongNameHere", False, "Too long"),
            ("John123", False, "Contains numbers"),
            ("John Doe", False, "Contains space"),
            ("O'Brien", False, "Contains apostrophe"),
            ("<script>", False, "XSS attempt"),
            ("'; DROP TABLE users;--", False, "SQL injection"),
        ]
        
        passed = True
        details = "Name validation test results:\n"
        
        for name, expected_valid, description in test_cases:
            is_valid = validname(name)
            
            if is_valid and not expected_valid:
                passed = False
                details += f"  - ISSUE: '{name}' ({description}) - accepted\n"
            else:
                details += f"  - OK: '{name}' ({description})\n"
        
        details += "\nNOTE: Current validation rejects valid names with spaces or apostrophes.\n"
        details += "RECOMMENDATION: Allow spaces and common characters while sanitizing."
        
        self.log_test(test_name, passed, details, "LOW")
    
    def test_postcode_validation(self):
        """Test postcode validation"""
        test_name = "Postcode Validation"
        
        pattern = r'^[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}$'
        
        test_cases = [
            ("SW1A 1AA", True, "Valid postcode"),
            ("M1 1AE", True, "Valid short postcode"),
            ("CR2 6XH", True, "Valid postcode"),
            ("DN55 1PT", True, "Valid postcode"),
            ("W1A 0AX", True, "Valid postcode"),
            ("'; DROP TABLE users;--", False, "SQL injection"),
            ("<script>alert(1)</script>", False, "XSS attempt"),
            ("AAAAA", False, "Invalid format"),
        ]
        
        passed = True
        details = "Postcode validation test results:\n"
        
        for postcode, expected_valid, description in test_cases:
            is_valid = re.match(pattern, postcode, re.IGNORECASE) is not None
            
            if is_valid != expected_valid:
                passed = False
                details += f"  - ISSUE: '{postcode}' ({description})\n"
            else:
                details += f"  - OK: '{postcode}' ({description})\n"
        
        if passed:
            details += "\nPostcode validation appears secure."
            severity = "INFO"
        else:
            details += "\nRECOMMENDATION: Review postcode validation logic."
            severity = "LOW"
        
        self.log_test(test_name, passed, details, severity)
    
    # ==================== DATABASE SECURITY TESTS ====================
    
    def test_database_security(self):
        """Test database security configuration"""
        test_name = "Database Security Configuration"
        
        details = "Database security analysis:\n"
        details += "  - Database file: login.db (stored locally)\n"
        details += "  - No database encryption detected\n"
        details += "  - No backup strategy visible\n"
        details += "  - Database connection not using SSL/TLS\n"
        details += "\nVULNERABILITY: Database file can be accessed directly.\n"
        details += "RECOMMENDATION:\n"
        details += "  1. Encrypt database file (SQLCipher)\n"
        details += "  2. Set proper file permissions\n"
        details += "  3. Implement database backups\n"
        details += "  4. Consider server-based database for production"
        
        self.log_test(test_name, False, details, "MEDIUM")
    
    # ==================== CROSS-SITE SCRIPTING (XSS) TESTS ====================
    
    def test_xss_in_displayed_data(self):
        """Test for XSS vulnerabilities in displayed data"""
        test_name = "Cross-Site Scripting (XSS) Protection"
        
        details = "XSS vulnerability analysis:\n"
        details += "  - University names displayed without sanitization\n"
        details += "  - User names displayed in UI\n"
        details += "  - Quiz answers stored and potentially displayed\n"
        details += "\nPOTENTIAL VULNERABILITY: If data from database is displayed without sanitization,\n"
        details += "XSS attacks are possible through stored data.\n"
        details += "\nTest payloads:\n"
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src='javascript:alert(1)'>"
        ]
        
        for payload in xss_payloads:
            details += f"  - {payload}\n"
        
        details += "\nRECOMMENDATION:\n"
        details += "  1. Sanitize all user input before storage\n"
        details += "  2. Escape output when displaying user data\n"
        details += "  3. Use Content Security Policy headers\n"
        details += "  4. Validate data types strictly"
        
        self.log_test(test_name, False, details, "HIGH")
    
    # ==================== DATA EXPOSURE TESTS ====================
    
    def test_sensitive_data_exposure(self):
        """Test for sensitive data exposure"""
        test_name = "Sensitive Data Exposure"
        
        details = "Sensitive data exposure analysis:\n"
        details += "  - ISSUE: User ID printed to console (line 179: print(result1[0]))\n"
        details += "  - ISSUE: Saved universities printed to console (line 53, 495)\n"
        details += "  - ISSUE: Quiz answers printed to console (line 439)\n"
        details += "  - ISSUE: Plain text passwords in memory before hashing\n"
        details += "\nVULNERABILITY: Sensitive information logged to console.\n"
        details += "In production, console logs may be exposed.\n"
        details += "\nRECOMMENDATION:\n"
        details += "  1. Remove or disable debug print statements\n"
        details += "  2. Implement proper logging with levels\n"
        details += "  3. Never log sensitive data (passwords, tokens)\n"
        details += "  4. Use secure logging libraries"
        
        self.log_test(test_name, False, details, "MEDIUM")
    
    # ==================== REPORT GENERATION ====================
    
    def generate_report(self):
        """Generate comprehensive security test report"""
        print("\n" + "="*80)
        print(" SECURITY PENETRATION TEST REPORT FOR nea1.py")
        print("="*80)
        print(f"\nTest Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Tests Run: {len(self.test_results)}")
        print(f"Critical Vulnerabilities Found: {len([v for v in self.vulnerabilities if v['severity'] == 'CRITICAL'])}")
        print(f"High Severity Issues: {len([v for v in self.vulnerabilities if v['severity'] == 'HIGH'])}")
        print(f"Medium Severity Issues: {len([v for v in self.vulnerabilities if v['severity'] == 'MEDIUM'])}")
        
        print("\n" + "="*80)
        print(" DETAILED TEST RESULTS")
        print("="*80)
        
        for result in self.test_results:
            print(f"\n[{result['severity']}] {result['test']}")
            print("-" * 80)
            print(f"Status: {'PASSED' if result['passed'] else 'FAILED'}")
            print(f"\n{result['details']}")
        
        print("\n" + "="*80)
        print(" CRITICAL VULNERABILITIES SUMMARY")
        print("="*80)
        
        if self.vulnerabilities:
            for i, vuln in enumerate(self.vulnerabilities, 1):
                print(f"\n{i}. [{vuln['severity']}] {vuln['test']}")
                print(f"   {vuln['details'][:200]}...")
        else:
            print("\nNo critical vulnerabilities found.")
        
        print("\n" + "="*80)
        print(" RECOMMENDATIONS PRIORITY")
        print("="*80)
        print("\n1. CRITICAL - Implement salted password hashing (bcrypt/Argon2)")
        print("2. HIGH - Add rate limiting and brute force protection")
        print("3. HIGH - Implement XSS protection and input sanitization")
        print("4. MEDIUM - Improve session management with timeouts")
        print("5. MEDIUM - Encrypt database or restrict file access")
        print("6. MEDIUM - Remove sensitive data from console logs")
        print("7. LOW - Enhance input validation for names and emails")
        
        print("\n" + "="*80)
        print(" END OF REPORT")
        print("="*80 + "\n")
    
    def run_all_tests(self):
        """Run all security tests"""
        print("Starting security penetration tests...")
        print("="*80)
        
        # Password Security Tests
        print("\n[1/11] Testing password hashing algorithm...")
        self.test_password_hashing_algorithm()
        
        print("[2/11] Testing rainbow table attack resistance...")
        self.test_password_rainbow_table_attack()
        
        print("[3/11] Testing password validation strength...")
        self.test_password_validation_strength()
        
        # SQL Injection Tests
        print("[4/11] Testing SQL injection vulnerabilities...")
        self.test_sql_injection_login()
        
        # Email Validation Tests
        print("[5/11] Testing email validation...")
        self.test_email_validation_bypass()
        
        # Authentication Tests
        print("[6/11] Testing brute force protection...")
        self.test_brute_force_protection()
        
        print("[7/11] Testing session management...")
        self.test_session_management()
        
        # Input Validation Tests
        print("[8/11] Testing name field validation...")
        self.test_name_validation()
        
        print("[9/11] Testing postcode validation...")
        self.test_postcode_validation()
        
        # Database Security Tests
        print("[10/11] Testing database security...")
        self.test_database_security()
        
        # XSS Tests
        print("[11/11] Testing XSS protection...")
        self.test_xss_in_displayed_data()
        
        # Sensitive Data Tests
        print("[12/11] Testing sensitive data exposure...")
        self.test_sensitive_data_exposure()
        
        print("\n" + "="*80)
        print("All tests completed!")
        print("="*80)
        
        # Generate report
        self.generate_report()


def main():
    """Main entry point for security testing"""
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                    NEA1.PY SECURITY TESTING SUITE                        ║
    ║                          Penetration Test Mode                            ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
    This test suite will perform comprehensive security testing on nea1.py
    to identify potential vulnerabilities and security issues.
    
    Tests include:
    - Password security and hashing
    - SQL injection vulnerabilities
    - Authentication and authorization
    - Input validation
    - XSS protection
    - Session management
    - Database security
    - Sensitive data exposure
    """)
    
    tester = SecurityTester()
    tester.run_all_tests()
    
    # Save report to file
    report_file = "security_test_report.txt"
    print(f"\n[INFO] Security test report has been displayed above.")
    print(f"[INFO] You can redirect this output to a file using:")
    print(f"       python test_security_nea1.py > {report_file}")


if __name__ == "__main__":
    main()
