import os
import sys

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath("__file__")))) # elérésí út beállítása
sys.path.append(PROJECT_PATH)

from src.wealthdistribution.server import server

server.launch() # szerver indítása
