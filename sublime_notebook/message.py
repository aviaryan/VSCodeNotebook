"""
Print statements
"""

def print_info(msg):
	if msg.find('\n') > -1:
		print('\n' + msg)
	else:
		print('\n[[ ' + msg + ' ]]')

def print_err(msg):
	if msg.find('\n') > -1:
		print('\n' + msg)
	else:
		print('\n<< ' + msg + ' >>')
