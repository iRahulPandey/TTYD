"""
Reusable UI components for the Streamlit application.
"""
import pandas as pd
import streamlit as st

from utils.image_handler import is_image_path
from config import EXAMPLE_QUESTIONS


def render_data_preview(df):
    """
    Render a preview of the loaded dataframe.
    
    Args:
        df (pandas.DataFrame): Dataframe to preview
    """
    if df is None:
        return
        
    with st.expander("Data Preview"):
        st.dataframe(df.head(10), use_container_width=True)
        st.text(f"Total rows: {len(df)}")
        
        # Display column types
        col_types = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes.values,
            'Non-Null Count': df.count().values,
            'Null Count': df.isna().sum().values
        })
        st.dataframe(col_types, use_container_width=True)


def render_conversation_messages(conversation):
    """
    Render the conversation history with questions and responses.
    
    Args:
        conversation (list): List of conversation entries (tuples of query, response, code)
    """
    for i, (query, response, code) in enumerate(conversation):
        # Display question
        st.markdown(f'<div class="question"><strong>You:</strong> {query}</div>', 
                   unsafe_allow_html=True)
        
        # Display answer container start
        st.markdown('<div class="answer">', unsafe_allow_html=True)
        
        # Process different types of responses
        if isinstance(response, pd.DataFrame):
            st.write("<strong>AI:</strong> Here's the result:", unsafe_allow_html=True)
            st.dataframe(response, use_container_width=True)
        elif is_image_path(response):
            # This is a path to an image
            st.write("<strong>AI:</strong> Here's the visualization you requested:", 
                    unsafe_allow_html=True)
            try:
                st.image(response)
            except Exception as e:
                st.error(f"Could not display image: {str(e)}")
        elif isinstance(response, dict) and 'plotly' in response:
            st.write("<strong>AI:</strong> Here's the visualization you requested:", 
                    unsafe_allow_html=True)
            st.plotly_chart(response['plotly'], use_container_width=True)
        else:
            # Text response
            st.write(f"<strong>AI:</strong> {response}", unsafe_allow_html=True)
        
        # Display answer container end
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Code viewer
        with st.expander(f"View generated code for Query {i+1}"):
            st.markdown('<p class="code-header">Python code used to generate this response:</p>', 
                       unsafe_allow_html=True)
            st.code(code, language="python")


def render_example_questions():
    """Render the list of example questions."""
    st.markdown("### Example questions you can ask:")
    
    # Display questions in a more readable format
    for question in EXAMPLE_QUESTIONS:
        st.markdown(f"- {question}")


def render_download_buttons(conversation, raw_df, container=None):
    """
    Render download buttons for conversation history and data.
    
    Args:
        conversation (list): The conversation history
        raw_df (pandas.DataFrame): The raw dataframe for download
        container: Optional container to render buttons in (e.g., st.sidebar)
    """
    # Use the provided container or default to st
    ui = container or st
    
    # Fixed boolean check to avoid DataFrame truth value error
    if not conversation and raw_df is None:
        return
    
    # Render download data button if dataframe exists
    if raw_df is not None:
        csv = raw_df.to_csv(index=False)
        ui.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name="exported_data.csv",
            mime="text/csv"
        )

    # Render download conversation button if conversation exists
    if conversation:
        conversation_text = "\n\n".join([
            f"User: {query}\nAI: {str(response)}\nCode:\n{code}" 
            for query, response, code in conversation
        ])
        ui.download_button(
            label="Download Conversation",
            data=conversation_text,
            file_name="conversation_history.txt",
            mime="text/plain"
        )