import os
import sys
# Set the path for project imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from pygasfrac.app import create_app

app = create_app()
