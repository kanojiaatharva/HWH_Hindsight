"""
Pytest configuration for the Incident Déjà Vu backend test suite.
"""
import sys
import os

# Ensure the backend directory is on the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
