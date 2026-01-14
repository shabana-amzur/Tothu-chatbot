"""
Authentication Module
---------------------
Handles user authentication and session management for Streamlit.
"""

import streamlit as st
from database.db_connection import SessionLocal
from database import crud


def check_authentication():
    """
    Check if user is authenticated.
    
    Returns:
        bool: True if authenticated, False otherwise
    """
    return st.session_state.get("authenticated", False)


def get_current_user():
    """
    Get current logged-in user.
    
    Returns:
        dict: User information or None
    """
    return st.session_state.get("user", None)


def login_page():
    """
    Display modern login modal with dark theme - matching reference design.
    Layout: Logo → Welcome heading → Login form → OR divider → Social buttons → Sign up link
    """
    # Apply custom CSS for modern login modal
    st.markdown("""
    <style>
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stSidebar"] {display: none;}
        [data-testid="stDecoration"] {display: none;}
        [data-testid="stToolbar"] {display: none;}
        
        /* Full-screen background */
        .stApp {
            background-color: #F5F6F8 !important;
        }
        
        /* Center the entire container */
        .main .block-container {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            min-height: 100vh !important;
            padding: 1rem !important;
            max-width: 100% !important;
        }
        
        /* Remove all default spacing */
        .element-container {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Hide all form labels */
        .stTextInput > label, 
        .stForm > label,
        label {
            display: none !important;
        }
        
        /* Single unified card */
        div[data-testid="column"]:nth-child(2) {
            background: #FFFFFF !important;
            padding: 2.5rem 2rem !important;
            border-radius: 32px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12) !important;
            border: 1px solid rgba(0, 0, 0, 0.08) !important;
            max-width: 400px !important;
            margin: 0 auto !important;
        }
        
        /* Logo icon */
        .logo-icon {
            width: 64px;
            height: 64px;
            background: #1C1C1E;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            margin: 0 auto 1.25rem;
        }
        
        /* Welcome heading */
        h1 {
            color: #1C1C1E !important;
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            text-align: center !important;
            margin: 0 0 0.5rem 0 !important;
            padding: 0 !important;
            line-height: 1.3 !important;
        }
        
        /* Subtitle */
        .subtitle {
            text-align: center;
            color: #6E6E73;
            font-size: 0.875rem;
            margin-bottom: 1.75rem;
        }
        
        /* Input fields */
        .stTextInput {
            margin-bottom: 0.75rem !important;
        }
        
        .stTextInput input {
            background-color: #F5F5F7 !important;
            color: #1C1C1E !important;
            border: 1px solid #E5E5EA !important;
            border-radius: 8px !important;
            padding: 0.75rem 1rem !important;
            font-size: 0.9375rem !important;
            height: 44px !important;
            width: 100% !important;
            transition: all 0.2s;
        }
        
        .stTextInput input:focus {
            border-color: #007AFF !important;
            box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1) !important;
            outline: none !important;
            background-color: #FFFFFF !important;
        }
        
        .stTextInput input::placeholder {
            color: #8E8E93 !important;
        }
        
        /* Sign in button */
        .stForm button {
            width: 100% !important;
            background-color: #1C1C1E !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.75rem 1.5rem !important;
            height: 44px !important;
            font-size: 0.9375rem !important;
            font-weight: 600 !important;
            transition: all 0.2s;
            margin: 0.75rem 0 1.25rem 0 !important;
        }
        
        form button:hover {
            background-color: #2C2C2E !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(28, 28, 30, 0.3);
        }
        
        /* Divider */
        .divider-container {
            display: flex;
            align-items: center;
            margin: 0 0 1rem 0;
        }
        
        .divider-line {
            flex: 1;
            height: 1px;
            background: #E5E5EA;
        }
        
        .divider-text {
            color: #8E8E93;
            font-size: 0.8125rem;
            padding: 0 0.75rem;
        }
        
        /* Social buttons */
        .social-btn button {
            width: 100% !important;
            background-color: #F5F5F7 !important;
            color: #1C1C1E !important;
            border: 1px solid #E5E5EA !important;
            border-radius: 8px !important;
            padding: 0.6875rem 1rem !important;
            height: 44px !important;
            font-size: 0.9375rem !important;
            font-weight: 500 !important;
            margin-bottom: 0.625rem !important;
            transition: all 0.2s;
        }
        
        .social-btn button:hover {
            background-color: #EBEBF0 !important;
            border-color: #D1D1D6 !important;
        }
        
        /* Sign up link */
        .signup-link {
            text-align: center;
            color: #6E6E73;
            font-size: 0.875rem;
            margin-top: 1rem;
        }
        
        .signup-link button {
            background: none !important;
            color: #007AFF !important;
            border: none !important;
            padding: 0 !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            text-decoration: none !important;
            cursor: pointer;
            height: auto !important;
            margin: 0 !important;
        }
        
        .signup-link button:hover {
            text-decoration: underline !important;
            background: none !important;
        }
        
        /* Error/Success messages */
        .stAlert {
            background-color: #FFF3CD !important;
            border: 1px solid #FFE69C !important;
            color: #856404 !important;
            border-radius: 8px !important;
            margin-bottom: 0.75rem !important;
            padding: 0.75rem !important;
            font-size: 0.875rem !important;
        }
        
        /* Form container - no spacing */
        .stForm {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Back button */
        .back-button button {
            background-color: transparent !important;
            color: #007AFF !important;
            border: none !important;
            padding: 0.5rem 0 !important;
            font-size: 0.875rem !important;
            text-align: left !important;
            margin: 0 0 1rem 0 !important;
            height: auto !important;
            border-radius: 0 !important;
        }
        
        .back-button button:hover {
            background-color: transparent !important;
            text-decoration: underline;
        }
        
        /* Hide column gaps */
        [data-testid="column"] {
            padding: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "show_signup" not in st.session_state:
        st.session_state.show_signup = False
    
    # Create centered layout
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if not st.session_state.show_signup:
            # ===== LOGIN FORM =====
            # Logo icon
            st.markdown('<div class="logo-icon">🦜</div>', unsafe_allow_html=True)
            
            # Welcome heading
            st.markdown('# Welcome to Tothu')
            st.markdown('<div class="subtitle">Unlock all features by logging in</div>', unsafe_allow_html=True)
            
            # Login form
            with st.form("login_form", clear_on_submit=False):
                username = st.text_input("username", placeholder="Enter your username", key="login_username", label_visibility="collapsed")
                password = st.text_input("password", type="password", placeholder="Enter your password", key="login_password", label_visibility="collapsed")
                
                submit = st.form_submit_button("Sign in")
                
                if submit:
                    if not username or not password:
                        st.error("Please enter both username and password.")
                    else:
                        db = SessionLocal()
                        try:
                            user = crud.authenticate_user(db, username, password)
                            if user:
                                st.session_state.authenticated = True
                                st.session_state.user = {
                                    "id": user.id,
                                    "username": user.username,
                                    "email": user.email,
                                    "full_name": user.full_name
                                }
                                st.success("Welcome back!")
                                st.rerun()
                            else:
                                st.error("Invalid username or password.")
                        finally:
                            db.close()
            
            # Divider
            st.markdown("""
            <div class="divider-container">
                <div class="divider-line"></div>
                <div class="divider-text">or</div>
                <div class="divider-line"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Social login buttons
            st.markdown('<div class="social-btn">', unsafe_allow_html=True)
            if st.button("🔍 Continue with Google", key="google_login", use_container_width=True):
                st.info("🔜 Google login coming soon!")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="social-btn">', unsafe_allow_html=True)
            if st.button("⚫ Continue with GitHub", key="github_login", use_container_width=True):
                st.info("🔜 GitHub login coming soon!")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Sign up link
            st.markdown('<div class="signup-link">Don\'t have an account? ', unsafe_allow_html=True)
            if st.button("Sign up now", key="go_to_signup"):
                st.session_state.show_signup = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            # ===== SIGN UP FORM =====
            st.markdown('<div class="back-button">', unsafe_allow_html=True)
            if st.button("← Back to Login", key="back_to_login"):
                st.session_state.show_signup = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Logo icon
            st.markdown('<div class="logo-icon">🦜</div>', unsafe_allow_html=True)
            
            st.markdown('# Create Account')
            st.markdown('<div class="subtitle">Join Tothu community</div>', unsafe_allow_html=True)
            
            with st.form("signup_form", clear_on_submit=False):
                email = st.text_input("email", placeholder="your.name@amzur.com", key="signup_email", label_visibility="collapsed")
                username = st.text_input("username", placeholder="Choose a username", key="signup_username", label_visibility="collapsed")
                full_name = st.text_input("name", placeholder="Your full name", key="signup_fullname", label_visibility="collapsed")
                password = st.text_input("password", type="password", placeholder="Create a password", key="signup_password", label_visibility="collapsed")
                confirm_password = st.text_input("confirm", type="password", placeholder="Confirm your password", key="signup_confirm", label_visibility="collapsed")
                
                submit = st.form_submit_button("Create Account")
                
                if submit:
                    if not all([email, username, full_name, password, confirm_password]):
                        st.error("Please fill in all fields.")
                    elif not email.endswith("@amzur.com"):
                        st.error("Please use your Amzur email address")
                    elif password != confirm_password:
                        st.error("Passwords do not match.")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        db = SessionLocal()
                        try:
                            if crud.get_user_by_email(db, email):
                                st.error("Email already registered.")
                            elif crud.get_user_by_username(db, username):
                                st.error("Username already taken.")
                            else:
                                user = crud.create_user(db, email, username, password, full_name)
                                st.success("✅ Account created! Please login.")
                                st.session_state.show_signup = False
                                st.balloons()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                        finally:
                            db.close()



def logout():
    """Logout current user."""
    st.session_state.authenticated = False
    st.session_state.user = None
    if "messages" in st.session_state:
        del st.session_state.messages
    st.rerun()
