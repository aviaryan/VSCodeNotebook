import json
import os
import time
from subprocess import check_output, STDOUT
from vscode_notebook import SETTINGS_PATH, VERSION
from .message import print_err, print_info


class Settings:
	"""
	Settings module
	"""
	default_json = {
		'public_folders': ['*'],
		'private_folders': ['diary'],
		'is_encrypted': False,
		'version': VERSION,
		'do_git_backup': False,
		'git_push_interval_minutes': 1440,
		'last_git_push': 0
	}
	json = default_json.copy()
	where_star = 'public'
	file = SETTINGS_PATH

	def __init__(self, file=None):
		if file:
			self.file = file
		self.load_file()

	def load_file(self):
		"""
		Loads file as JSON
		"""
		try:
			fp = open(self.file, 'r')
			data = fp.read()
			self.json = json.loads(data)
			fp.close()
			self.find_star()
		except Exception as e:
			# load default settings
			print_err('JSON Exception occurred: ' + str(e))

	def find_star(self):
		if Settings._find_in_array('*', self.json['private_folders']):
			self.where_star = 'private'
		else:  
			# default behavior public
			self.where_star = 'public'

	def check_folder_private(self, dirname):
		st = Settings._find_in_array(dirname, self.json['private_folders'])
		if st:
			return True
		st = Settings._find_in_array(dirname, self.json['public_folders'])
		if st:
			return False
		# star situation
		return True if self.where_star == 'private' else False

	def change_encrypted_status(self, status):
		self.load_file()
		self.json['is_encrypted'] = status
		self.save_settings()

	def get_encrypted_status(self):
		return self.json['is_encrypted']

	def save_settings(self):
		Settings._write_settings(self.json, self.file)

	def upgrade_settings(self):
		if VERSION > self.json['version']:
			new = self.default_json.copy()
			new.update(self.json)  # only adds new keys
			self.json = new.copy()
			self.json['version'] = VERSION  # upgrade version again
			self.save_settings()
			return True
		return False

	def is_git_setup(self):
		curpath = os.path.dirname(os.path.realpath(__file__))
		git_path = curpath.rstrip('/\\') + '/../.git'
		# print(git_path)
		return os.path.isdir(git_path)

	def do_git_push(self):
		if not self.json['do_git_backup']:
			return False
		mins = int(round(time.time()) / 60.0)
		if mins < (self.json['last_git_push'] + self.json['git_push_interval_minutes']):
			return False
		# start backup
		print_info('Starting git backup')
		# check remote
		out = check_output("git remote", shell=True).decode()
		if not out:
			print_err('Error with git remote: ' + str(out))
			return False
		if out and out.find('notebookbackup') == -1:
			print_err('notebookbackup remote not found')
			return False
		# push to remote
		print_info('Pushing to remote')
		commit_msg = "auto backup " + str(mins)
		out = check_output("git add -A && git commit -m \"{}\" && git push notebookbackup master".format(commit_msg), 
			stderr=STDOUT, shell=True).decode()
		print_info('GIT LOG:\n\n' + out)
		self.json['last_git_push'] = mins
		self.save_settings()

	@staticmethod
	def _find_in_array(item, arr):
		status = False
		for i in arr:
			if item == i:
				status = True
				break
		return status

	@staticmethod
	def _create_default_file():
		Settings._write_settings(Settings.json, Settings.file)

	@staticmethod
	def _write_settings(setting, file):
		data = json.dumps(setting, indent=4, sort_keys=True)
		fp = open(file, 'w')
		fp.write(data)
		fp.close()
