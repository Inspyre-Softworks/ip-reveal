import os
import pickle

def generate_version(type):
    """
    
    Part of the development workflow for IP reveal.
    
    Creates a VERSION pickle to be shipped w/ ip-reveal
    
    Args:
        type (str): Can be your choice of; major, minor, patch, pr, pr-build

    Returns:
        None

    """
