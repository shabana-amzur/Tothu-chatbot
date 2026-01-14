import streamlit as st
from database.db_connection import SessionLocal
from database.crud import create_user, authenticate_user


def check_authentication():
    """Check if user is authenticated."""
    return st.session_state.get("authenticated", False)


def get_current_user():
    """Get current logged-in user."""
    if st.session_state.get("authenticated", False):
        return {
            "id": st.session_state.get("user_id"),
            "username": st.session_state.get("username"),
            "email": st.session_state.get("email")
        }
    return None


def logout():
    """Logout the current user."""
    st.session_state.authenticated = False
    if 'user_id' in st.session_state:
        del st.session_state.user_id
    if 'username' in st.session_state:
        del st.session_state.username
    if 'email' in st.session_state:
        del st.session_state.email
    st.rerun()


def login_page():
    # Initialize session state
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    if 'show_forgot_password' not in st.session_state:
        st.session_state.show_forgot_password = False
    if 'login_attempt' not in st.session_state:
        st.session_state.login_attempt = 0
    if 'error_message' not in st.session_state:
        st.session_state.error_message = ""
    
    # Custom CSS for beautiful dark theme
    st.markdown("""
    <style>
        /* Hide ALL Streamlit chrome */
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="stDecoration"] {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
        [data-testid="stHeader"] {display: none !important;}
        [data-testid="stStatusWidget"] {display: none !important;}
        .stApp > header {display: none !important;}
        iframe {display: none !important;}
        
        /* Remove the empty div container */
        .main > div:first-child:empty {
            display: none !important;
        }
        div[data-testid="stVerticalBlock"] > div:empty {
            display: none !important;
        }
        
        /* Full-screen dark background */
        .stApp {
            background-color: #000000 !important;
        }
        [data-testid="stAppViewContainer"] {
            background: #000000 !important;
        }
        .main {
            background: #000000 !important;
        }
        
        /* Center content and remove all padding */
        .main .block-container {
            padding: 2rem 1rem !important;
            margin: 0 auto !important;
            max-width: 100% !important;
        }
        
        /* Center everything */
        .main .block-container {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            min-height: 100vh !important;
            padding: 1rem !important;
            max-width: 100% !important;
        }
        
        /* Dark theme inputs */
        .stTextInput input {
            background: #2A2A2A !important;
            border: 1px solid #3A3A3A !important;
            border-radius: 8px !important;
            padding: 0 14px !important;
            height: 42px !important;
            color: #FFFFFF !important;
            font-size: 14px !important;
        }
        .stTextInput input:focus {
            border-color: #0A84FF !important;
            background: #252525 !important;
        }
        .stTextInput input::placeholder {
            color: #6B6B6B !important;
        }
        
        /* Hide labels */
        .stTextInput > label {
            display: none !important;
        }
        
        /* Hide buttons with 'hidden' in their text */
        .stButton {
            position: relative;
        }
        .stButton button[data-testid="baseButton-secondary"],
        .stButton button[kind="secondary"] {
            display: none !important;
        }
        /* Hide any button containing 'hidden' */
        div[data-testid="column"] > div > div > div > button:nth-child(n) {
            color: transparent;
            height: 0;
            padding: 0;
            margin: 0;
            border: none;
            overflow: hidden;
        }
        div[data-testid="column"] > div > div > div > button:first-of-type:last-of-type {
            /* This targets buttons that are the only button in their container */
        }
        /* Only show Sign in button */
        button[kind="primary"] {
            display: block !important;
            color: #FFFFFF !important;
            height: 42px !important;
        }
        
        /* Button styling */
        .stButton button {
            background: #0A84FF !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            height: 42px !important;
            width: 100% !important;
            font-size: 15px !important;
            font-weight: 500 !important;
            transition: opacity 0.2s !important;
        }
        .stButton button:hover {
            opacity: 0.85 !important;
        }
        
        /* Hide hidden buttons */
        button:has-text("hidden") {
            display: none !important;
        }
        .stButton:has(button[aria-label*="hidden"]) {
            display: none !important;
        }
        
        /* Small link button styling (for forgot password and signup) */
        button[kind="secondary"] {
            background: transparent !important;
            color: #0A84FF !important;
            border: none !important;
            padding: 0 !important;
            height: auto !important;
            font-size: 13px !important;
            font-weight: 400 !important;
            text-decoration: none !important;
        }
        button[kind="secondary"]:hover {
            text-decoration: underline !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    if st.session_state.show_forgot_password:
        # FORGOT PASSWORD VIEW
        col1, col2, col3 = st.columns([1, 1.2, 1])
        
        with col2:
            st.markdown("""
            <div style="background: #1A1A1A; border-radius: 14px; padding: 32px 28px; box-shadow: 0 4px 24px rgba(0, 0, 0, 0.5); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            """, unsafe_allow_html=True)
            
            # Heading
            st.markdown("""
            <h1 style="font-size: 20px; font-weight: 600; color: #FFFFFF; text-align: center; margin-bottom: 8px;">Reset Password</h1>
            <p style="text-align: center; color: #8E8E93; font-size: 13px; margin-bottom: 24px;">Enter your email to reset your password</p>
            """, unsafe_allow_html=True)
            
            # Back button
            if st.button("← Back to login", key="back_from_forgot"):
                st.session_state.show_forgot_password = False
                st.session_state.error_message = ""
                st.rerun()
            
            # Email input
            reset_email = st.text_input("Email", placeholder="your.name@amzur.com", key="reset_email")
            
            if st.button("Send Reset Link", key="send_reset", use_container_width=True):
                if reset_email:
                    import re
                    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', reset_email):
                        st.error("Please enter a valid email address")
                    else:
                        # TODO: Implement actual password reset logic
                        # For now, just show a success message
                        st.success("✅ If an account exists with this email, you will receive a password reset link shortly.")
                else:
                    st.error("⚠️ Please enter your email address")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    elif not st.session_state.show_signup:
        # LOGIN VIEW - Using Streamlit components with beautiful styling
        col1, col2, col3 = st.columns([1, 1.2, 1])
        
        with col2:
            # Container div
            st.markdown("""
            <div style="background: #1A1A1A; border-radius: 14px; padding: 32px 28px; box-shadow: 0 4px 24px rgba(0, 0, 0, 0.5); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            """, unsafe_allow_html=True)
            
            # Heading
            st.markdown("""
            <h1 style="font-size: 20px; font-weight: 600; color: #FFFFFF; text-align: center; margin-bottom: 8px;">Welcome to Tothu</h1>
            <p style="text-align: center; color: #8E8E93; font-size: 13px; margin-bottom: 24px;">Unlock smarter responses</p>
            """, unsafe_allow_html=True)
            
            # Error message
            if st.session_state.error_message:
                st.markdown(f"""
                <div style="background: #3A1A1A; border: 1px solid #FF453A; color: #FF453A; padding: 10px; border-radius: 8px; font-size: 13px; margin-bottom: 14px; text-align: center;">
                    {st.session_state.error_message}
                </div>
                """, unsafe_allow_html=True)
            
            # Login form with unique keys
            username = st.text_input("Username", placeholder="Username", key=f"username_{st.session_state.login_attempt}")
            password = st.text_input("Password", type="password", placeholder="Password", key=f"password_{st.session_state.login_attempt}")
            
            # Forgot password link - right aligned (hidden button approach)
            st.markdown('<div style="text-align: right; margin: -12px 0 16px 0;"><a href="?forgot=true" style="color: #0A84FF; text-decoration: none; font-size: 13px;">Forgot password?</a></div>', unsafe_allow_html=True)
            
            # Check query params for forgot password
            try:
                query_params = st.query_params
                if 'forgot' in query_params:
                    st.session_state.show_forgot_password = True
                    st.query_params.clear()
                    st.rerun()
            except:
                pass
            
            # Sign in button
            if st.button("Sign in", key=f"signin_{st.session_state.login_attempt}", use_container_width=True):
                if username and password:
                    if len(username) < 3:
                        st.session_state.error_message = "Username must be at least 3 characters"
                        st.session_state.login_attempt += 1
                        st.rerun()
                    elif len(password) < 6:
                        st.session_state.error_message = "Password must be at least 6 characters"
                        st.session_state.login_attempt += 1
                        st.rerun()
                    else:
                        db = SessionLocal()
                        try:
                            user = authenticate_user(db, username, password)
                            if user:
                                st.session_state.authenticated = True
                                st.session_state.user_id = user.id
                                st.session_state.username = user.username
                                st.session_state.email = user.email
                                st.session_state.error_message = ""
                                st.rerun()
                            else:
                                st.session_state.error_message = "❌ Invalid username or password"
                                st.session_state.login_attempt += 1
                                st.rerun()
                        finally:
                            db.close()
                else:
                    st.session_state.error_message = "⚠️ Please enter both username and password"
                    st.session_state.login_attempt += 1
                    st.rerun()
            
            # Divider
            st.markdown("""
            <div style="display: flex; align-items: center; margin: 20px 0; gap: 12px;">
                <div style="flex: 1; height: 1px; background: #3A3A3A;"></div>
                <div style="color: #6B6B6B; font-size: 13px;">or</div>
                <div style="flex: 1; height: 1px; background: #3A3A3A;"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Social buttons
            st.markdown("""
            <button disabled style="width: 100%; height: 42px; background: #2A2A2A; border: 1px solid #3A3A3A; border-radius: 8px; color: #FFFFFF; font-size: 14px; cursor: not-allowed; opacity: 0.6; margin-bottom: 10px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">🔍 Continue with Google</button>
            <button disabled style="width: 100%; height: 42px; background: #2A2A2A; border: 1px solid #3A3A3A; border-radius: 8px; color: #FFFFFF; font-size: 14px; cursor: not-allowed; opacity: 0.6; margin-bottom: 10px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">⚫ Continue with GitHub</button>
            """, unsafe_allow_html=True)
            
            # Signup link - inline hyperlink style like Qwen
            st.markdown("""
            <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #3A3A3A; color: #8E8E93; font-size: 13px;">
                Don't have an account? <a href="?signup=true" style="color: #0A84FF; text-decoration: underline; font-weight: 400;">Sign up</a>
            </div>
            """, unsafe_allow_html=True)
            
            # Check query params for signup
            try:
                query_params = st.query_params
                if 'signup' in query_params:
                    st.session_state.show_signup = True
                    st.session_state.error_message = ""
                    st.query_params.clear()
                    st.rerun()
            except:
                pass
            
            # Terms
            st.markdown("""
            <div style="text-align: center; margin-top: 16px; color: #6B6B6B; font-size: 11px; line-height: 1.5;">
                By continuing, you agree to Tothu's<br/>
                <a href="#" style="color: #6B6B6B; text-decoration: underline;">Terms of Service</a> and <a href="#" style="color: #6B6B6B; text-decoration: underline;">Privacy Policy</a>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    else:
        # SIGNUP VIEW
        col1, col2, col3 = st.columns([1, 1.2, 1])
        
        with col2:
            st.markdown("""
            <div style="background: #1A1A1A; border-radius: 14px; padding: 32px 28px; box-shadow: 0 4px 24px rgba(0, 0, 0, 0.5); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            """, unsafe_allow_html=True)
            
            # Logo
            st.markdown("""
            <div style="width: 48px; height: 48px; background: #2A2A2A; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 28px; margin: 0 auto 24px;">🦜</div>
            """, unsafe_allow_html=True)
            
            # Heading
            st.markdown("""
            <h1 style="font-size: 20px; font-weight: 600; color: #FFFFFF; text-align: center; margin-bottom: 8px;">Create Account</h1>
            <p style="text-align: center; color: #8E8E93; font-size: 13px; margin-bottom: 24px;">Join Tothu to start your AI journey</p>
            """, unsafe_allow_html=True)
            
            # Back button
            if st.button("← Back to login", key="back_to_login"):
                st.session_state.show_signup = False
                st.session_state.error_message = ""
                st.rerun()
            
            # Signup form
            email = st.text_input("Email", placeholder="your.name@amzur.com", key="signup_email")
            username = st.text_input("Username", placeholder="Choose a username", key="signup_username")
            full_name = st.text_input("Full Name", placeholder="Your full name", key="signup_fullname")
            password = st.text_input("Password", type="password", placeholder="Create a password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="signup_confirm")
            
            if st.button("Create Account", key="create_account", use_container_width=True):
                if email and username and full_name and password and confirm_password:
                    import re
                    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                        st.error("Please enter a valid email address")
                    elif len(username) < 3:
                        st.error("Username must be at least 3 characters")
                    elif not re.match(r'^[a-zA-Z0-9_]+$', username):
                        st.error("Username can only contain letters, numbers, and underscores")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters")
                    elif password != confirm_password:
                        st.error("❌ Passwords do not match")
                    else:
                        db = SessionLocal()
                        try:
                            user = create_user(
                                db=db,
                                email=email,
                                username=username,
                                password=password,
                                full_name=full_name
                            )
                            st.success(f"✅ Account created! Welcome, {user.username}!")
                            st.session_state.authenticated = True
                            st.session_state.user_id = user.id
                            st.session_state.username = user.username
                            st.session_state.email = user.email
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ {str(e)}")
                        finally:
                            db.close()
                else:
                    st.error("⚠️ Please fill in all fields")
            
            st.markdown("</div>", unsafe_allow_html=True)
