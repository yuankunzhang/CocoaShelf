import sys
import os
import site
import uwsgi

sys.stdin = sys.stdout

site.addsitedir('/var/www/cocoa/venv/lib/python2.6/site-packages')

BASE_DIR = os.path.join(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from cocoa import create_app
from cocoa.config import ProductionConfig

application = create_app(ProductionConfig)
uwsgi.applications = {'/':application}
