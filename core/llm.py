"""
Core functionality for LLM integration.
"""
from langchain_community.llms import Ollama


def create_ollama_llm(model_name):
    """
    Create an Ollama LLM instance with the specified model name.
    
    Args:
        model_name (str): Name of the Ollama model to use
        
    Returns:
        Ollama: Configured Ollama LLM instance
    """
    try:
        # Create the Ollama LLM with the specified model
        return Ollama(model=model_name)
    except Exception as e:
        # If there's an error, log it and use default parameters
        print(f"Error creating Ollama LLM: {str(e)}")
        return Ollama(model="mixtral")  # Fallback to mixtral