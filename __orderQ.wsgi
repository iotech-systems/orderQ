import sys

APP_PATH = "/opt/iotech/orderQ"
sys.path.insert(0, APP_PATH)

# -- import app from run file --
from run import app as application
