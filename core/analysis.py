"""
Core functionality for data analysis using SmartDataframe.
"""
import streamlit as st
from utils.image_handler import make_persistent_copy, is_image_path


class DataAnalyzer:
    """
    Class for managing data analysis with SmartDataframe.
    Handles query processing, response management, and conversation history.
    """
    
    def __init__(self, smart_df=None):
        """
        Initialize the DataAnalyzer.
        
        Args:
            smart_df: Optional SmartDataframe instance
        """
        self.smart_df = smart_df
        self.conversation = []
        self.current_query = None
        self.processing = False
        
    def set_dataframe(self, smart_df):
        """
        Set the SmartDataframe to use for analysis.
        
        Args:
            smart_df: The SmartDataframe instance
        """
        self.smart_df = smart_df
        
    def process_query(self, query):
        """
        Process a user query using the SmartDataframe.
        
        Args:
            query (str): The user's query
            
        Returns:
            tuple: (success, error_message)
        """
        if self.smart_df is None:
            return False, "No dataframe loaded. Please upload a CSV file first."
            
        if not query:
            return False, "Query cannot be empty."
            
        try:
            # Always send the query to the LLM for processing
            response = self.smart_df.chat(query)
            code = self.smart_df.last_code_executed
            
            # Handle image responses
            if is_image_path(response):
                persistent_path = make_persistent_copy(response)
                if persistent_path:
                    response = persistent_path
            
            # Add to conversation history
            self.conversation.append((query, response, code))
            return True, None
                
        except Exception as e:
            error_msg = f"Error analyzing data: {str(e)}"
            return False, error_msg
            
    def get_conversation_history(self):
        """
        Get the conversation history.
        
        Returns:
            list: List of conversation entries
        """
        return self.conversation
        
    def clear_conversation(self):
        """Clear the conversation history."""
        self.conversation = []