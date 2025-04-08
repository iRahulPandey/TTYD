"""
Utility functions for monkey patching system operations to prevent
unwanted behaviors like automatic image viewer opening.
"""
import os


def override_system_function():
    """
    Override the os.system function to prevent external applications 
    from opening automatically.
    
    Returns:
        function: The original os.system function for reference
    """
    # Store the original function
    original_system = os.system
    
    # Define our replacement function
    def no_op_system(cmd):
        """
        Custom replacement for os.system that blocks commands
        attempting to open external applications.
        
        Args:
            cmd (str): The command to be executed
            
        Returns:
            int: Return code (0 for blocked commands)
        """
        # If the command is trying to open an application, block it
        if any(opener in cmd for opener in ["open ", "xdg-open", "start "]):
            return 0
        
        # Otherwise, let the original function handle it
        return original_system(cmd)
    
    # Replace the original function with our version
    os.system = no_op_system
    
    return original_system


def apply_system_patches():
    """Apply all necessary system function patches."""
    # Override os.system to prevent opening external applications
    override_system_function()