import streamlit as st
from typing import Optional, Dict, Any
from utils.database import authenticate_user, create_user, init_db

def init_session_state() -> None:
    """Initializes authentication keys in Streamlit session_state."""
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "nav_page" not in st.session_state:
        st.session_state["nav_page"] = "Home"
    if "last_prediction" not in st.session_state:
        st.session_state["last_prediction"] = None

def get_current_user() -> Optional[Dict[str, Any]]:
    """Returns the authenticated user dict or None."""
    init_session_state()
    return st.session_state.get("user")

def is_authenticated() -> bool:
    """Returns True if a user is currently logged in."""
    init_session_state()
    return bool(st.session_state.get("logged_in") and st.session_state.get("user"))

def is_admin() -> bool:
    """Returns True if the authenticated user has an 'admin' role."""
    user = get_current_user()
    return bool(user and user.get("role") == "admin")

def login(user: Dict[str, Any]) -> None:
    """Sets session state to logged in with the provided user profile."""
    st.session_state["user"] = user
    st.session_state["logged_in"] = True

def logout() -> None:
    """Clears user session and logs out."""
    st.session_state["user"] = None
    st.session_state["logged_in"] = False
    st.session_state["last_prediction"] = None
    st.session_state["nav_page"] = "Home"

def require_auth() -> bool:
    """
    Renders an authentication gate if user is not authenticated.
    Returns True if user is authenticated, False otherwise.
    """
    if not is_authenticated():
        st.warning("🔒 Authentication required. Please log in or register to access this feature.")
        return False
    return True

def require_admin() -> bool:
    """
    Renders an authorization gate for administrator-only operations.
    Returns True if user is admin, False otherwise.
    """
    if not is_authenticated():
        st.warning("🔒 Please log in as an Administrator to view this console.")
        return False
    if not is_admin():
        st.error("⛔ Access Denied: You do not possess administrator privileges.")
        return False
    return True
