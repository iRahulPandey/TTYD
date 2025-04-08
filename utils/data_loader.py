"""
Utilities for loading and preprocessing data.
"""
import pandas as pd
import streamlit as st


def load_csv_data(file):
    """
    Load data from a CSV file.
    
    Args:
        file: A file-like object containing CSV data
        
    Returns:
        pandas.DataFrame or None: The loaded dataframe or None if loading failed
    """
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None


def get_data_summary(df):
    """
    Get a summary of the dataframe for display.
    
    Args:
        df (pandas.DataFrame): The dataframe to summarize
        
    Returns:
        dict: Summary statistics about the dataframe
    """
    if df is None:
        return None
        
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isna().sum().sum(),
        "memory_usage": df.memory_usage(deep=True).sum() / (1024 * 1024)  # MB
    }