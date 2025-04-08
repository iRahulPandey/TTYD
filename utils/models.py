"""
Utilities for managing LLM models.
"""
import subprocess
import streamlit as st

from config import FALLBACK_MODELS


def get_ollama_models():
    """
    Fetch the list of available Ollama models.
    
    Returns:
        list: List of available model names
    """
    try:
        # Execute the Ollama list command
        result = subprocess.run(
            ['ollama', 'list'], 
            capture_output=True, 
            text=True, 
            check=False
        )
        
        # Check if command executed successfully
        if result.returncode != 0:
            raise RuntimeError(f"ollama list failed: {result.stderr}")
            
        # Parse the output to extract model names
        lines = result.stdout.strip().split('\n')
        if len(lines) <= 1:  # Only header line or empty
            return FALLBACK_MODELS
            
        # Skip header line and extract the first column (model name)
        models = [line.split()[0] for line in lines[1:]]
        return models if models else FALLBACK_MODELS
        
    except (subprocess.SubprocessError, FileNotFoundError, IndexError) as e:
        st.error(f"Error fetching Ollama models: {str(e)}")
        return FALLBACK_MODELS