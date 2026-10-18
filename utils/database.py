import sqlite3
import hashlib
import secrets
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
import os
from config import DATABASE_PATH

def get_connection() -> sqlite3.Connection:
    """Returns a SQLite connection with row_factory set to sqlite3.Row."""
    conn = sqlite3.connect(str(DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    """Hashes a password using PBKDF2-HMAC-SHA256 with a unique cryptographic salt."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        200_000
    )
    return f"{salt}${key.hex()}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verifies a stored password hash against a provided plaintext password."""
    try:
        salt, key_hex = stored_password.split('$', 1)
        expected_key = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt.encode('utf-8'),
            200_000
        )
        return secrets.compare_digest(key_hex, expected_key.hex())
    except Exception:
        return False

def init_db() -> None:
    """Initializes database tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'student',
        created_at TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        timestamp TEXT NOT NULL,
        study_hours REAL NOT NULL,
        attendance REAL NOT NULL,
        sleep_hours REAL NOT NULL,
        internet_usage REAL NOT NULL,
        assignments_completed REAL NOT NULL,
        previous_score REAL NOT NULL,
        exam_score REAL NOT NULL,
        prediction_result TEXT NOT NULL,
        placement_probability REAL NOT NULL,
        confidence REAL NOT NULL,
        risk_level TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

def create_user(
    username: str,
    email: str,
    full_name: str,
    password: str,
    role: str = "student"
) -> Tuple[bool, str]:
    """
    Creates a new user. Default role is 'student'.
    Returns (success, message).
    """
    username = username.strip().lower()
    email = email.strip().lower()
    full_name = full_name.strip()

    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if not email or "@" not in email or "." not in email:
        return False, "Please enter a valid email address."
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if not full_name:
        return False, "Full name cannot be empty."

    valid_roles = ["student", "admin"]
    if role not in valid_roles:
        role = "student"

    conn = get_connection()
    cursor = conn.cursor()

    try:
        pw_hash = hash_password(password)
        now = datetime.now().isoformat()
        cursor.execute(
            """
            INSERT INTO users (username, email, full_name, password_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (username, email, full_name, pw_hash, role, now)
        )
        conn.commit()
        return True, "User registered successfully."
    except sqlite3.IntegrityError as e:
        err_msg = str(e).lower()
        if "username" in err_msg:
            return False, f"Username '{username}' is already taken."
        elif "email" in err_msg:
            return False, f"Email '{email}' is already registered."
        return False, "Username or email is already registered."
    except Exception as e:
        return False, f"Database error: {str(e)}"
    finally:
        conn.close()

def authenticate_user(username_or_email: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticates a user by username or email. Returns user dict on success, None on failure."""
    identifier = username_or_email.strip().lower()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username, email, full_name, password_hash, role, created_at
        FROM users
        WHERE username = ? OR email = ?
        """,
        (identifier, identifier)
    )
    row = cursor.fetchone()
    conn.close()

    if row and verify_password(row["password_hash"], password):
        return {
            "id": row["id"],
            "username": row["username"],
            "email": row["email"],
            "full_name": row["full_name"],
            "role": row["role"],
            "created_at": row["created_at"]
        }
    return None

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves a user profile by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, email, full_name, role, created_at FROM users WHERE id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def list_all_users() -> List[Dict[str, Any]]:
    """Lists all users for the administrator console."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, email, full_name, role, created_at FROM users ORDER BY created_at DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_user_role(user_id: int, new_role: str) -> bool:
    """Updates user role (admin only)."""
    if new_role not in ["student", "admin"]:
        return False
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def delete_user(user_id: int) -> bool:
    """Deletes a user and cascades their prediction history."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def reset_user_password(user_id: int, new_password: str) -> Tuple[bool, str]:
    """Resets a user's password (administrator operation)."""
    if not new_password or len(new_password) < 6:
        return False, "Password must be at least 6 characters long."
    conn = get_connection()
    cursor = conn.cursor()
    pw_hash = hash_password(new_password)
    cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (pw_hash, user_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    if affected > 0:
        return True, "Password reset successfully."
    return False, "User not found."

def save_prediction(
    user_id: int,
    inputs: Dict[str, float],
    prediction_result: str,
    placement_probability: float,
    confidence: float,
    risk_level: str,
    notes: Optional[str] = None
) -> int:
    """Saves a prediction entry to SQLite database and returns the new row ID."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO predictions (
            user_id, timestamp, study_hours, attendance, sleep_hours,
            internet_usage, assignments_completed, previous_score,
            exam_score, prediction_result, placement_probability,
            confidence, risk_level, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            now,
            float(inputs.get("study_hours", 0.0)),
            float(inputs.get("attendance", 0.0)),
            float(inputs.get("sleep_hours", 0.0)),
            float(inputs.get("internet_usage", 0.0)),
            float(inputs.get("assignments_completed", 0.0)),
            float(inputs.get("previous_score", 0.0)),
            float(inputs.get("exam_score", 0.0)),
            prediction_result,
            float(placement_probability),
            float(confidence),
            risk_level,
            notes
        )
    )
    conn.commit()
    pred_id = cursor.lastrowid
    conn.close()
    return pred_id

def get_user_predictions(user_id: int, limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieves prediction history for an authenticated student (data isolation)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM predictions
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, limit)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_prediction_by_id(pred_id: int, user_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Retrieves a single prediction record. If user_id is provided, enforces student ownership."""
    conn = get_connection()
    cursor = conn.cursor()
    if user_id is not None:
        cursor.execute(
            "SELECT * FROM predictions WHERE id = ? AND user_id = ?",
            (pred_id, user_id)
        )
    else:
        cursor.execute("SELECT * FROM predictions WHERE id = ?", (pred_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def delete_prediction(pred_id: int, user_id: Optional[int] = None) -> bool:
    """Deletes a prediction record. If user_id is given, ensures ownership."""
    conn = get_connection()
    cursor = conn.cursor()
    if user_id is not None:
        cursor.execute("DELETE FROM predictions WHERE id = ? AND user_id = ?", (pred_id, user_id))
    else:
        cursor.execute("DELETE FROM predictions WHERE id = ?", (pred_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def clear_user_predictions(user_id: int) -> int:
    """Clears all predictions for a specific student."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions WHERE user_id = ?", (user_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected

def get_admin_system_metrics() -> Dict[str, Any]:
    """Calculates aggregate system statistics for the administrator dashboard."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    total_users = cursor.fetchone()["total_users"]

    cursor.execute("SELECT COUNT(*) AS total_students FROM users WHERE role = 'student'")
    total_students = cursor.fetchone()["total_students"]

    cursor.execute("SELECT COUNT(*) AS total_admins FROM users WHERE role = 'admin'")
    total_admins = cursor.fetchone()["total_admins"]

    cursor.execute("SELECT COUNT(*) AS total_preds FROM predictions")
    total_preds = cursor.fetchone()["total_preds"]

    cursor.execute("SELECT COUNT(*) AS placed_preds FROM predictions WHERE prediction_result = 'Placed'")
    placed_preds = cursor.fetchone()["placed_preds"]

    cursor.execute("""
        SELECT p.*, u.username, u.full_name
        FROM predictions p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.id DESC
        LIMIT 50
    """)
    recent_activity = [dict(r) for r in cursor.fetchall()]

    conn.close()

    placement_rate = (placed_preds / total_preds * 100) if total_preds > 0 else 0.0

    return {
        "total_users": total_users,
        "total_students": total_students,
        "total_admins": total_admins,
        "total_predictions": total_preds,
        "placed_predictions": placed_preds,
        "placement_rate": placement_rate,
        "recent_activity": recent_activity
    }

def get_all_predictions_detailed(
    user_id: Optional[int] = None,
    outcome: Optional[str] = None,
    risk: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 200
) -> List[Dict[str, Any]]:
    """Retrieves full predictions with user metadata and dynamic filtering for administrative inspection."""
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT p.*, u.username, u.full_name, u.email
        FROM predictions p
        JOIN users u ON p.user_id = u.id
        WHERE 1=1
    """
    params = []

    if user_id:
        query += " AND p.user_id = ?"
        params.append(user_id)
    if outcome and outcome != "All":
        query += " AND p.prediction_result = ?"
        params.append(outcome)
    if risk and risk != "All":
        query += " AND p.risk_level = ?"
        params.append(risk)
    if search:
        s = f"%{search.strip().lower()}%"
        query += " AND (LOWER(u.username) LIKE ? OR LOWER(u.full_name) LIKE ? OR LOWER(u.email) LIKE ?)"
        params.extend([s, s, s])

    query += " ORDER BY p.id DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows
