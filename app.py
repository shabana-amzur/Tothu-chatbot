"""
Chatbot Application with Streamlit UI
--------------------------------------
Enhanced with PostgreSQL database and user authentication.
Features: ChatGPT-like interface, conversation management, dark/light mode.
"""

import streamlit as st
from llm.gemini_llm import GeminiLLM
from auth import check_authentication, get_current_user, login_page, logout
from database.db_connection import SessionLocal, init_db
from database import crud
from datetime import datetime

# Configure the Streamlit page
st.set_page_config(
    page_title="Tothu - AI Chatbot",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_database():
    """Initialize database tables if they don't exist."""
    try:
        init_db()
    except Exception as e:
        st.error(f"Database initialization error: {str(e)}")


def apply_custom_css(theme="light"):
    """Apply custom CSS for ChatGPT-like interface with theme support."""
    if theme == "dark":
        bg_color = "#212121"
        secondary_bg = "#2C2C2C"
        text_color = "#ECECF1"
        user_msg_bg = "#212121"
        assistant_msg_bg = "#212121"
        border_color = "#3E3E3E"
        input_bg = "#2C2C2C"
        sidebar_bg = "#171717"
        user_bubble = "#2A5C8C"
        assistant_bubble = "#2C2C2C"
        hover_bg = "#2A2A2A"
    else:
        bg_color = "#FFFFFF"
        secondary_bg = "#F9FAFB"
        text_color = "#1F2937"
        user_msg_bg = "#FFFFFF"
        assistant_msg_bg = "#FFFFFF"
        border_color = "#E5E7EB"
        input_bg = "#FFFFFF"
        sidebar_bg = "#F3F4F6"
        user_bubble = "#3B82F6"
        assistant_bubble = "#F3F4F6"
        hover_bg = "#F9FAFB"
    
    st.markdown(f"""
    <style>
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Overall app background */
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        
        /* Main container */
        .main .block-container {{
            padding-top: 3rem;
            padding-bottom: 2rem;
            max-width: 1200px;
            background-color: {bg_color};
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg};
            padding-top: 2rem;
        }}
        
        [data-testid="stSidebar"] .element-container {{
            color: {text_color};
        }}
        
        [data-testid="stSidebar"] h3 {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }}
        
        /* Chat message container */
        .stChatMessage {{
            background-color: transparent;
            border: none;
            padding: 1.5rem 0;
            margin-bottom: 0.5rem;
        }}
        
        /* User message - left aligned with blue bubble */
        .stChatMessage[data-testid="user-message"] {{
            background-color: {user_msg_bg};
        }}
        
        .stChatMessage[data-testid="user-message"] > div {{
            display: flex;
            justify-content: flex-start;
            max-width: 100%;
        }}
        
        .stChatMessage[data-testid="user-message"] .stMarkdown {{
            background-color: {user_bubble};
            color: white;
            padding: 0.875rem 1.25rem;
            border-radius: 20px;
            max-width: 75%;
            margin-left: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            font-size: 0.95rem;
            line-height: 1.5;
        }}
        
        /* Assistant message - right aligned with gray bubble */
        .stChatMessage[data-testid="assistant-message"] {{
            background-color: {assistant_msg_bg};
        }}
        
        .stChatMessage[data-testid="assistant-message"] > div {{
            display: flex;
            justify-content: flex-end;
            max-width: 100%;
        }}
        
        .stChatMessage[data-testid="assistant-message"] .stMarkdown {{
            background-color: {assistant_bubble};
            color: {text_color};
            padding: 0.875rem 1.25rem;
            border-radius: 20px;
            max-width: 75%;
            margin-right: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            font-size: 0.95rem;
            line-height: 1.5;
        }}
        
        /* Hide avatars for cleaner look */
        .stChatMessage img {{
            display: none;
        }}
        
        /* Buttons - cleaner style */
        .stButton button {{
            border-radius: 8px;
            border: 1px solid {border_color};
            transition: all 0.2s;
            background-color: transparent;
            color: {text_color};
            font-size: 0.875rem;
            padding: 0.5rem 1rem;
            font-weight: 500;
        }}
        
        .stButton button:hover {{
            background-color: {hover_bg};
            border-color: {border_color};
        }}
        
        /* Input box - modern style */
        .stChatInput {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: {bg_color};
            padding: 1.5rem;
            border-top: 1px solid {border_color};
        }}
        
        .stChatInput > div {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .stChatInput textarea {{
            background-color: {input_bg};
            color: {text_color};
            border: 1px solid {border_color};
            border-radius: 24px;
            padding: 1rem 1.5rem;
            font-size: 0.95rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }}
        
        .stChatInput textarea:focus {{
            border-color: #3B82F6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}
        
        /* Headings */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_color};
        }}
        
        /* Dividers */
        hr {{
            border-color: {border_color};
            margin: 1rem 0;
        }}
        
        /* Text elements */
        p, span, label {{
            color: {text_color};
        }}
        
        /* Info boxes */
        .stInfo {{
            background-color: {secondary_bg};
            color: {text_color};
            border: 1px solid {border_color};
        }}
        
        /* Markdown in sidebar */
        [data-testid="stSidebar"] .stMarkdown {{
            color: {text_color};
        }}
        
        /* Captions */
        .stCaption {{
            color: {text_color};
            opacity: 0.6;
            font-size: 0.85rem;
        }}
    </style>
    """, unsafe_allow_html=True)


def get_conversations(user_id: int):
    """Get all conversations for a user grouped by date."""
    db = SessionLocal()
    try:
        # Get all messages grouped by date
        messages = crud.get_user_messages(db, user_id)
        
        # Group messages by date
        conversations = {}
        for msg in messages:
            date_key = msg.timestamp.strftime("%Y-%m-%d")
            if date_key not in conversations:
                conversations[date_key] = []
            conversations[date_key].append(msg)
        
        return conversations
    except Exception as e:
        st.error(f"Error loading conversations: {str(e)}")
        return {}
    finally:
        db.close()


def load_chat_history_from_db(user_id: int, date_filter=None):
    """Load user's chat history from database, optionally filtered by date."""
    db = SessionLocal()
    try:
        messages = crud.get_user_messages(db, user_id)
        if date_filter:
            messages = [msg for msg in messages if msg.timestamp.strftime("%Y-%m-%d") == date_filter]
        st.session_state.messages = [
            {"role": msg.role, "content": msg.content, "timestamp": msg.timestamp}
            for msg in messages
        ]
    except Exception as e:
        st.error(f"Error loading chat history: {str(e)}")
        st.session_state.messages = []
    finally:
        db.close()


def save_message_to_db(user_id: int, role: str, content: str):
    """Save a message to the database."""
    db = SessionLocal()
    try:
        crud.create_message(db, user_id, role, content)
    except Exception as e:
        st.error(f"Error saving message: {str(e)}")
    finally:
        db.close()


def initialize_session_state():
    """
    Initialize Streamlit session state variables.
    
    Session state allows us to persist data across reruns of the app.
    This is crucial for maintaining chat history.
    """
    # Initialize theme
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    
    # Initialize current conversation date
    if "current_conversation" not in st.session_state:
        st.session_state.current_conversation = None
    
    # Initialize chat history if it doesn't exist
    # Load from database if user is logged in
    if "messages" not in st.session_state:
        user = get_current_user()
        if user:
            load_chat_history_from_db(user["id"])
        else:
            st.session_state.messages = []
    
    # Initialize the Gemini LLM if it doesn't exist
    # We only want to create this once, not on every rerun
    if "gemini_llm" not in st.session_state:
        try:
            st.session_state.gemini_llm = GeminiLLM(
                model_name="gemini-2.5-flash-lite",  # Using gemini-2.5-flash-lite model
                temperature=0.7
            )
        except Exception as e:
            # If there's an error (e.g., missing API key), show it to the user
            st.error(f"Failed to initialize Gemini LLM: {str(e)}")
            st.stop()  # Stop the app from running further


def display_chat_history():
    """
    Display all previous messages in the chat.
    
    This function iterates through the message history and displays
    each message with the appropriate styling (user vs assistant).
    """
    for message in st.session_state.messages:
        # message is a dictionary with 'role' and 'content' keys
        # role can be either 'user' or 'assistant'
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main():
    """
    Main function that runs the Streamlit app.
    
    This function handles the UI layout, user input, and interaction
    with the Gemini LLM.
    """
    # Initialize database
    initialize_database()
    
    # Check authentication
    if not check_authentication():
        login_page()
        return
    
    # User is authenticated - show chatbot
    user = get_current_user()
    
    # Initialize session state variables
    initialize_session_state()
    
    # Apply custom CSS theme
    apply_custom_css(st.session_state.theme)
    
    # Sidebar for conversations and settings
    with st.sidebar:
        # Header with theme toggle
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 💬 Chats")
        with col2:
            theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
            if st.button(theme_icon, help="Toggle theme", key="theme_toggle"):
                st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
                st.rerun()
        
        # New chat button
        if st.button("+ New Chat", use_container_width=True, key="new_chat_btn"):
            st.session_state.messages = []
            st.session_state.current_conversation = None
            st.rerun()
        
        st.divider()
        
        # Display conversations grouped by date
        conversations = get_conversations(user["id"])
        
        if conversations:
            # Get today's date
            today = datetime.now().strftime("%Y-%m-%d")
            
            for date_key in sorted(conversations.keys(), reverse=True):
                # Format date label
                if date_key == today:
                    date_label = "Today"
                else:
                    date_obj = datetime.strptime(date_key, "%Y-%m-%d")
                    date_label = date_obj.strftime("%b %d")
                
                st.markdown(f"**{date_label}**")
                
                # Show conversation preview
                messages = conversations[date_key]
                first_user_msg = next((msg for msg in messages if msg.role == "user"), None)
                preview = first_user_msg.content[:40] + "..." if first_user_msg and len(first_user_msg.content) > 40 else (first_user_msg.content if first_user_msg else "Empty conversation")
                
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(f"💬 {preview}", key=f"conv_{date_key}", use_container_width=True):
                        st.session_state.current_conversation = date_key
                        load_chat_history_from_db(user["id"], date_key)
                        st.rerun()
                with col2:
                    if st.button("🗑️", key=f"del_{date_key}", help="Delete"):
                        # Delete messages for this date
                        db = SessionLocal()
                        try:
                            # Delete messages from this date
                            all_msgs = crud.get_user_messages(db, user["id"])
                            for msg in all_msgs:
                                if msg.timestamp.strftime("%Y-%m-%d") == date_key:
                                    db.delete(msg)
                            db.commit()
                            
                            # Clear current view if it was this conversation
                            if st.session_state.current_conversation == date_key:
                                st.session_state.messages = []
                                st.session_state.current_conversation = None
                            
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                        finally:
                            db.close()
        else:
            st.info("No chat history yet")
        
        # Spacer to push account section to bottom
        st.markdown("<br>" * 5, unsafe_allow_html=True)
        
        st.divider()
        
        # User info section - compact
        st.markdown(f"**👤 {user['username']}**")
        st.caption(user['email'])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Logout", use_container_width=True, key="logout_btn"):
                logout()
        with col2:
            if st.button("Clear All", use_container_width=True, key="clear_all_btn"):
                db = SessionLocal()
                try:
                    crud.delete_user_messages(db, user["id"])
                    st.session_state.messages = []
                    st.session_state.current_conversation = None
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                finally:
                    db.close()
    
    # Main chat interface
    # Show welcome screen if no messages
    if not st.session_state.messages:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>Hi, I'm Tothu 🦜</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; opacity: 0.7;'>How can I help you today?</p>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
    else:
        # Display chat history (previous messages)
        display_chat_history()
    
    # Chat input field
    # This creates a text input at the bottom of the page
    user_input = st.chat_input("Type your message here...")
    
    # Process user input when they submit a message
    if user_input:
        # Validate that the input is not empty or just whitespace
        if user_input.strip() == "":
            st.warning("Please enter a valid message.")
            return
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now()
        })
        
        # Save user message to database
        save_message_to_db(user["id"], "user", user_input)
        
        # Update current conversation date
        st.session_state.current_conversation = datetime.now().strftime("%Y-%m-%d")
        
        # Get response from Gemini
        with st.chat_message("assistant"):
            # Show a loading spinner while waiting for the response
            with st.spinner("Thinking..."):
                try:
                    # Get the response from the Gemini LLM
                    response = st.session_state.gemini_llm.get_response(user_input)
                except Exception as e:
                    response = f"Sorry, I encountered an error: {str(e)}"
                    st.error(response)
            
            # Display the response
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now()
        })
        
        # Save assistant message to database
        save_message_to_db(user["id"], "assistant", response)


# This is the entry point of the application
# When you run `streamlit run app.py`, this block executes
if __name__ == "__main__":
    main()
