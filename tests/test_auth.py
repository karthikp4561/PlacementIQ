import pytest
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.database import (
    init_db,
    hash_password,
    verify_password,
    create_user,
    authenticate_user
)

def test_password_hashing():
    pw = "SuperSecret123!"
    hash1 = hash_password(pw)
    hash2 = hash_password(pw)
    # Different salts should produce distinct hash strings
    assert hash1 != hash2
    assert verify_password(hash1, pw) is True
    assert verify_password(hash2, pw) is True
    assert verify_password(hash1, "WrongPassword") is False

def test_user_registration_and_authentication():
    init_db()
    uid = uuid.uuid4().hex[:8]
    username = f"user_{uid}"
    email = f"{username}@test.com"
    password = "Password@123"

    success, msg = create_user(username, email, "Test User", password, role="student")
    assert success is True

    # Duplicate registration check
    dup_success, dup_msg = create_user(username, f"other_{uid}@test.com", "Test User", password)
    assert dup_success is False
    assert "already taken" in dup_msg.lower()

    # Authenticate with username
    auth_user = authenticate_user(username, password)
    assert auth_user is not None
    assert auth_user["username"] == username
    assert auth_user["role"] == "student"

    # Authenticate with email
    auth_user_email = authenticate_user(email, password)
    assert auth_user_email is not None
    assert auth_user_email["id"] == auth_user["id"]

    # Authenticate with wrong password
    assert authenticate_user(username, "InvalidPass") is None
