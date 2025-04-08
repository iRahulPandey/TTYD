"""
Main Streamlit application UI.
"""
import streamlit as st

from config import APP_TITLE, APP_LAYOUT
from core.analysis import DataAnalyzer
from core.dataframe import create_smart_dataframe
from core.llm import create_ollama_llm
from ui.components import (render_data_preview, render_conversation_messages,
                                      render_example_questions, render_download_buttons)
from ui.styles import apply_custom_css
from utils.data_loader import load_csv_data
from utils.models import get_ollama_models


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = DataAnalyzer()
    if 'raw_df' not in st.session_state:
        st.session_state.raw_df = None


def handle_query_submission():
    """Handle user query submission."""
    query = st.session_state.user_input
    st.session_state.user_input = ""  # Clear input field
    
    # Add a custom message that we can control
    status_placeholder = st.empty()
    status_placeholder.info(f"Processing: {query}")
    
    analyzer = st.session_state.analyzer
    success, error = analyzer.process_query(query)
    
    # Clear the status message
    status_placeholder.empty()
    
    if not success and error:
        st.error(error)


def handle_file_upload(file, model_name):
    """
    Handle CSV file upload and initialization.
    
    Args:
        file: Uploaded file object
        model_name (str): Name of the LLM model to use
    
    Returns:
        bool: Whether the upload was successful
    """
    df = load_csv_data(file)
    if df is None:
        return False
        
    # Store the raw dataframe
    st.session_state.raw_df = df
    
    # Create LLM
    llm = create_ollama_llm(model_name)
    
    # Create SmartDataframe
    smart_df = create_smart_dataframe(df, llm)
    
    # Update the analyzer with the new SmartDataframe
    st.session_state.analyzer.set_dataframe(smart_df)
    return True


def render_sidebar():
    """Render the sidebar UI."""
    st.sidebar.title("Settings")
    
    # File uploader
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])
    
    # Model selection
    available_models = get_ollama_models()
    model = st.sidebar.selectbox("Select LLM Model", available_models)
    
    # Process file upload
    if uploaded_file is not None:
        if handle_file_upload(uploaded_file, model):
            st.sidebar.success("Data loaded successfully!")
            if st.session_state.raw_df is not None:
                st.sidebar.write(f"Rows: {len(st.session_state.raw_df)}, "
                              f"Columns: {len(st.session_state.raw_df.columns)}")
    
    # Add a separator
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Actions")
    
    # Clear conversation button
    if st.sidebar.button("Clear Conversation"):
        st.session_state.analyzer.clear_conversation()
        st.rerun()
    
    # Add a separator before Downloads section
    st.sidebar.markdown("---")
    
    # Render download buttons in sidebar
    st.sidebar.markdown("### Downloads")
    render_download_buttons(
        st.session_state.analyzer.get_conversation_history(),
        st.session_state.raw_df,
        container=st.sidebar  # Pass sidebar as the container
    )


def render_main_content():
    """Render the main content area."""
    st.title(APP_TITLE)
    st.write("Upload a CSV file and ask questions about your data!")
    
    # Display data preview if available
    if st.session_state.raw_df is not None:
        render_data_preview(st.session_state.raw_df)
    
    # Display conversation
    conversation = st.session_state.analyzer.get_conversation_history()
    render_conversation_messages(conversation)
    
    # Query input
    st.text_input(
        "Ask a question about your data:",
        key="user_input",
        on_change=handle_query_submission
    )
    
    # Example questions
    render_example_questions()


def run_app():
    """Run the Streamlit application."""
    # Configure the page
    st.set_page_config(page_title=APP_TITLE, layout=APP_LAYOUT)
    
    # Apply custom CSS
    apply_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Render the sidebar
    render_sidebar()
    
    # Render the main content
    render_main_content()