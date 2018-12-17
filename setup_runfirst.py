#!/usr/bin/env python

# TODO
# ensure all modules are actually installed
# not the current priority

#import pip
from os import path, listdir, makedirs

# def import_or_install(package):
#     try:
#         __import__(package)
#     except ImportError:
#         pip.main(['install', package])

if not path.exists('nosen_extracted'):
	makedirs('nosen_extracted')
if not path.exists('bull_extracted'):
	makedirs('bull_extracted')
if not path.exists('bear_extracted'):
	makedirs('bear_extracted')
if not path.exists('files_to_extract'):
	makedirs('files_to_extract')