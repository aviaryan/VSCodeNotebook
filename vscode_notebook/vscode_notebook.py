import os
from sys import exit
from .cryptlib import get_file_list, encode, update_file, get_key, decode
from .message import print_info, print_err
from .settings import Settings
from vscode_notebook import SETTINGS_PATH


def get_first_time_key():
	key = get_key()
	print('Re-enter key')
	key2 = get_key()
	if key != key2:
		print_info('Keys don\'t match, exiting')
		exit(1)
	return key2


def main():
	"""
	Executes Notebook
	"""
	if not os.path.exists(SETTINGS_PATH):
		# new case
		# or decrypted state in power fail
		print_info('Not encrypted, encrypting ....')
		# create settings
		print_info(
			'Created settings.json in vscode_notebook/ directory.\n' +
			'By default, only the "diary" directory is privated (encrypted), you can change this setting by editing settings.json.\n' +
			'See the docs for more info.'
		)
		Settings._create_default_file()
		# get password
		print_info('Starting encryption process')
		key = get_first_time_key()
		update_file(encode, get_file_list(), key)
		# update encryption status
		sts = Settings()
		sts.change_encrypted_status(True)
		print_info('VSCode Notebook setup complete')
	else:
		# get settings
		sts = Settings()
		# check Notebook settings version
		check = sts.upgrade_settings()
		if check:
			print_info('settings.json upgraded to current version')
		# decrypt
		key = ''
		if sts.get_encrypted_status():
			# already encrypted
			print_info('Encrypted. Enter key to unlock')
			key = get_key()
			failStatus = update_file(decode, get_file_list(), key)
			if failStatus:
				print_err('You entered wrong key. Please try again.')
				exit(2)
			# remove encryption status
			sts.change_encrypted_status(False)
			# decoded, wait to close
			print_info('Notes have been decrypted')
		else:
			print_info('Notes are already decrypted')
		# now decrypted
		ans = ''
		while (True):
			ans = input('Press "e" to encrypt\nPress "d" to leave decrypted\n> ')
			if ans == 'd' or ans == 'e':
				if ans == 'e' and key == '':  # already decrypt case
					key = get_first_time_key()
				break
		if ans == 'e':
			# encrypt
			st = update_file(encode, get_file_list(), key)
			if st:
				print_err('Something went wrong while encrypting')
				exit(3)
			sts.change_encrypted_status(True)
			print_info('Notes encrypted')
			# do git push
			if sts.is_git_setup():
				sts.do_git_push()
		else:
			# disable notebook
			# exit as-is
			print_info('Notes have been left decrypted')
			pass
