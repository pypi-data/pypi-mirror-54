"""Default configuration

Use env var to override
"""
import os 

DEBUG = True
SECRET_KEY = "changeme"

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/neocortex.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

GRAPH_DATABASE = os.environ.get('GRAPH_DATABASE')
GRAPH_USER = os.environ.get('GRAPH_USER')
GRAPH_PASSWORD = os.environ.get('GRAPH_PASSWORD')