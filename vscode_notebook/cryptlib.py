import base64
import os
import re
from getpass import getpass
from .settings import Settings
from .message import print_err


EXTRA_STR = 'ENCo0D#DT{xTCh$cKe>'
ENCODED_IDF = '=*=EnC0d3dH3aDer==*'

# Vigenere's Cipher: http://stackoverflow.com/a/38223403

def encode(key, clear):
    if clear.startswith(ENCODED_IDF):  # already encoded, no need to encode
        return clear
    clear += EXTRA_STR  # used to check if decrypt is correct
    # encode string
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return ENCODED_IDF + base64.urlsafe_b64encode("".join(enc).encode()).decode()


def decode(key, enc):
    st = ''
    if not enc.startswith(ENCODED_IDF):  # not encoded, so not decode
        return enc
    enc = enc[len(ENCODED_IDF):]  # trim out idf
    # decode string
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    st = "".join(dec)
    # check if correctly decoded
    if not st.endswith(EXTRA_STR):
        return None
    else:
        return st[:-1 * len(EXTRA_STR)]


def get_file_list():
    listFiles = []
    sts = Settings()
    # loop through directory
    for dirpath, dnames, fnames in os.walk('./'):
        dirname = dirpath.replace('./', '', 1)
        dirname = re.sub(r'/.*$', '', dirname)
        # print(dirname)
        if dirname.startswith('.'):  # hidden like .git
            continue
        if not sts.check_folder_private(dirname):
            continue
        for f in fnames:
            if not (f.endswith('.txt') or f.endswith('.md')):
                continue
            listFiles.append(os.path.join(dirpath, f))
    # print(listFiles)
    return listFiles


def update_file(funcptr, flist, key):
    failed = False
    for file in flist:
        fptr = open(file, 'r')
        data = fptr.read()
        fptr.close()
        fptr = open(file, 'w')
        newData = funcptr(key, data)
        if newData is None:
            newData = data
            failed = True
            print_err('Failed decrypting %s' % file)
        fptr.write(newData)
        fptr.close()
        # check if failed
        if failed:
            break
    return failed


def get_key():
    key = ''
    while key == '':
        key = getpass('Enter key > ')
    return key
