"""
Core functionality for managing SmartDataframes.
"""
import pandas as pd
from pandasai import SmartDataframe
from pandasai.responses.response_parser import ResponseParser

from config import DATAFRAME_CONFIG


class CaptureResponseParser(ResponseParser):
    """
    Custom response parser that captures results without displaying them.
    
    This prevents PandasAI from automatically displaying results, allowing
    our application to handle the display in a more controlled manner.
    """
    
    def __init__(self, context) -> None:
        """
        Initialize the response parser.
        
        Args:
            context: The PandasAI context
        """
        super().__init__(context)
        
    def format_dataframe(self, result):
        """
        Format a dataframe result.
        
        Args:
            result (dict): The result containing a dataframe
            
        Returns:
            pd.DataFrame: The dataframe result
        """
        return result["value"]
        
    def format_plot(self, result):
        """
        Format a plot result.
        
        Args:
            result (dict): The result containing a plot
            
        Returns:
            str: The path to the generated plot
        """
        return result["value"]
        
    def format_other(self, result):
        """
        Format other types of results.
        
        Args:
            result (dict): The result
            
        Returns:
            Any: The result value
        """
        return result["value"]


def create_smart_dataframe(df, llm):
    """
    Create a SmartDataframe with the given dataframe and LLM.
    
    Args:
        df (pd.DataFrame): The dataframe to analyze
        llm: The language model to use
        
    Returns:
        SmartDataframe: The configured smart dataframe
    """
    # Start with the default configuration
    config = DATAFRAME_CONFIG.copy()
    
    # Add the LLM and response parser
    config.update({
        "llm": llm,
        "response_parser": CaptureResponseParser,
    })
    
    try:
        # Create the SmartDataframe with our configuration
        smart_df = SmartDataframe(df, config=config)
        return smart_df
    except Exception as e:
        # If the full configuration fails, try a minimal configuration
        fallback_config = {"llm": llm, "verbose": True}
        return SmartDataframe(df, config=fallback_config)