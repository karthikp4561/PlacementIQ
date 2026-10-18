#!/usr/bin/env python
"""
PlacementIQ — Administrator Initialization Utility
Usage:
    python init_admin.py
    python init_admin.py --username admin --email admin@placementiq.edu --password YourSecurePassword
"""
import sys
import os
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils.database import init_db, create_user, get_connection, hash_password

def main():
    parser = argparse.ArgumentParser(description="Initialize or reset Administrator account for PlacementIQ.")
    parser.add_argument("--username", default=os.getenv("ADMIN_USERNAME", "admin"), help="Admin username")
    parser.add_argument("--email", default=os.getenv("ADMIN_EMAIL", "admin@placementiq.edu"), help="Admin email")
    parser.add_argument("--name", default=os.getenv("ADMIN_NAME", "System Administrator"), help="Admin full name")
    parser.add_argument("--password", default=os.getenv("ADMIN_PASSWORD", "Admin@12345"), help="Admin password")
    args = parser.parse_args()

    init_db()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, role FROM users WHERE username = ? OR email = ?", (args.username, args.email))
    existing = cursor.fetchone()

    if existing:
        print(f"Updating existing user '{existing['username']}' to role 'admin' with updated password...")
        pw_hash = hash_password(args.password)
        cursor.execute(
            "UPDATE users SET password_hash = ?, role = 'admin', full_name = ? WHERE id = ?",
            (pw_hash, args.name, existing["id"])
        )
        conn.commit()
        conn.close()
        print(f"[SUCCESS] Administrator '{args.username}' has been updated successfully.")
    else:
        conn.close()
        success, msg = create_user(
            username=args.username,
            email=args.email,
            full_name=args.name,
            password=args.password,
            role="admin"
        )
        if success:
            print(f"[SUCCESS] Administrator '{args.username}' created successfully.")
            print(f"Username: {args.username}")
            print(f"Email:    {args.email}")
            print(f"Role:     admin")
        else:
            print(f"[ERROR] Failed to create administrator: {msg}")

if __name__ == "__main__":
    main()
