import os
import sys
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
fileHandler = logging.FileHandler("logs.log")
fileHandler.setFormatter(formatter)
root.addHandler(fileHandler)
