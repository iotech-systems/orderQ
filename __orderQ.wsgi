import sys

APP_PATH = "/opt/iotech/orderQ"
sys.path.insert(0, APP_PATH)
from webapp import APP as application
