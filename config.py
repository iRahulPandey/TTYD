"""
Configuration settings for the AI Data Analyst application.
"""
import os
import tempfile
from pathlib import Path

# Application settings
APP_TITLE = "AI Data Analyst"
APP_LAYOUT = "wide"
DEFAULT_MODEL = "mixtral"
FALLBACK_MODELS = ["mixtral", "llama3", "gemma"]

# Directory configurations
ROOT_DIR = Path(__file__).parent.parent
PLOTS_DIR = os.path.join(ROOT_DIR, "saved_plots")
TEMP_DIR = tempfile.mkdtemp()

# Ensure required directories exist
os.makedirs(PLOTS_DIR, exist_ok=True)

# Environment variables for temporary files
os.environ["TMPDIR"] = TEMP_DIR
os.environ["TEMP"] = TEMP_DIR
os.environ["TMP"] = TEMP_DIR

# Smart Dataframe configuration
DATAFRAME_CONFIG = {
    "enable_cache": False,  # Disable PandasAI caching
    "verbose": False,  # Set to False to reduce console output
    "save_charts": False,
    "display_progress_bar": False,  # Disable progress bar
}

# Example questions to display in the UI
EXAMPLE_QUESTIONS = [
    "How many rows are in this dataset?",
    "What are the column names?",
    "Show me a summary of the numerical columns"
]