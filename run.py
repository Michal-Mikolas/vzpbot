from vzpbot import VZPBot
from model import Model, TooBigFile, NotSupportedExtension
from glob import glob
from datetime import datetime
from openpyxl.utils.exceptions import InvalidFileException
import os
from zipfile import BadZipFile
from pathlib import Path
import time
from datetime import datetime
import json
import sys


#     #
#     # ###### #      #####  ###### #####   ####
#     # #      #      #    # #      #    # #
####### #####  #      #    # #####  #    #  ####
#     # #      #      #####  #      #####       #
#     # #      #      #      #      #   #  #    #
#     # ###### ###### #      ###### #    #  ####

def load_config():
	conf_file = 'run.json'
	if len(sys.argv) > 1:
		conf_file = sys.argv[1]

	# Base config
	with open(conf_file, encoding='utf8') as config_file:
		config = json.load(config_file)

	# Finish
	return config

def str_datetime():
	return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


#     #
#  #  #  ####  #####  #    #
#  #  # #    # #    # #   #
#  #  # #    # #    # ####
#  #  # #    # #####  #  #
#  #  # #    # #   #  #   #
 ## ##   ####  #    # #    #

conf = load_config()

vzp = VZPBot()
vzp.init()

while True:
	files = glob(conf['path_inbox'] + "\\*.*")
	for file in files:
		#
		# Init
		#
		file_dir, file_name = os.path.split(file)
		print("\n[{:s}] {:s}".format(str_datetime(), file_name))

		try:
			model = Model(file)

		except (BadZipFile, ValueError, OverflowError, OSError, InvalidFileException, KeyError, TooBigFile, NotSupportedExtension) as e:
			print("[{:s}] {:s}: {:s}".format(str_datetime(), type(e).__name__, str(e)))
			continue

		#
		# Process all entries
		#
		while True:
			try:
				entry = model.next()
				if not entry:
					break
			except Exception as e:
				entry['insurance_type'] = 'ERROR'
				entry['insurance_text'] = "%s: %s" % (type(e).__name__, str(e))

			entry = vzp.fetch_insurance(entry)

			model.persist(entry)
 
		#
		# Save & move files
		#
		try:
			model.save("{:s}\\{:s}".format(conf['path_done'], file_name))
			os.replace(
				file,
				"{:s}\\{:s}".format(conf['path_backup'], file_name)
			)
		except PermissionError:
			print('ERROR: File is opened in another application!')

	#
	# Wait for new files
	#
	print("[{:s}] ...".format(str_datetime()))
	time.sleep(5)
