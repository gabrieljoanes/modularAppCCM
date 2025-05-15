# utils/version.py

"""
Version tracking module for the Transition Generator application.
Update the VERSION string below whenever logic changes in:
- transition_cleaner.py
- transition_validator.py
- geo_checker.py
- transitions.py or prompts
"""

VERSION = "v1.2.0"  # Increment this manually when logic or prompts are updated

def get_version():
    """
    Returns the current version of the application.
    """
    return VERSION
