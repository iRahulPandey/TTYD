"""
CSS styles and UI styling utilities for the Streamlit application.
"""

# CSS for styling the application components
CUSTOM_CSS = """
<style>
    /* Chat message containers */
    .question {
        padding: 10px;
        border-left: 5px solid #0066cc;
        margin-bottom: 10px;
        background-color: #f0f2f6;
        border-radius: 0 5px 5px 0;
    }
    
    .answer {
        padding: 10px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 10px;
        border-radius: 0 5px 5px 0;
    }
    
    /* Visualization container */
    .visualization-container {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        background-color: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .visualization-title {
        font-weight: bold;
        margin-bottom: 10px;
        color: #4CAF50;
    }
    
    /* Headers and content formatting */
    h1 {
        color: #0066cc;
        margin-bottom: 20px;
    }
    
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    
    .stButton button:hover {
        background-color: #45a049;
    }
    
    .code-header {
        font-size: 0.9em;
        color: #666;
        margin-bottom: 5px;
    }
</style>
"""


def apply_custom_css():
    """Apply custom CSS to the Streamlit application."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)