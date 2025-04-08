#!/usr/bin/env python3
"""
AI Data Analyst - Main Application Entry Point

A Streamlit application for analyzing data using natural language
through PandasAI, LangChain, and Ollama.
"""
import os
import sys

# Add the parent directory to sys.path to ensure imports work correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.monkey_patch import apply_system_patches
from ui.app import run_app


def main():
    """Application entry point."""
    # Apply necessary patches to prevent external windows
    apply_system_patches()
    
    # Run the Streamlit application
    run_app()


if __name__ == "__main__":
    main()