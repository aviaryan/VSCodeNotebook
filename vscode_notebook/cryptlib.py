import base64
import os
from traceback import print_exc
import re
from getpass import getpass
from .settings import Settings
from .message import print_err
from .pyaes import aes, AESModeOfOperationCTR


EXTRA_STR = 'ENCo0D#DT{xTCh$cKe>'
ENCODED_IDF = '=*=EnC0d3dH3aDer==*'
EXTRA_STR_2 = '3NCo0D#DT{xTCh$cKe>'
ENCODED_IDF_2 = '=*=3nC0d3dH3aDer==*'

# Vigenere's Cipher: http://stackoverflow.com/a/38223403

def encode_1(key, clear):
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


def decode_1(key, enc):
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


def encode(key, clear):
    if clear.startswith(ENCODED_IDF) or clear.startswith(ENCODED_IDF_2):  # already encoded, no need to encode
        return clear
    clear += EXTRA_STR_2  # used to check if decrypt is correct
    # encrypt string
    aes = AESModeOfOperationCTR(key_32(key))
    clear = bytes(clear, 'utf8')  # everyone writes in utf8
    ciphertext = aes.encrypt(clear)
    return ENCODED_IDF_2 + base64.urlsafe_b64encode(ciphertext).decode('iso-8859-1')


def decode(key, enc):
    st = ''
    if not (enc.startswith(ENCODED_IDF_2) or enc.startswith(ENCODED_IDF)):  # not encoded, so not decode
        return enc
    if enc.startswith(ENCODED_IDF):  # old version
        return decode_1(key, enc)
    # new version
    enc = enc[len(ENCODED_IDF_2):]  # trim out idf
    # https://wiki.python.org/moin/Python3UnicodeDecodeError
    # seems like the bytes created by pyaes are best decrypted using it
    enc = base64.urlsafe_b64decode(enc).decode('iso-8859-1')
    # decode string
    aes = AESModeOfOperationCTR(key_32(key))
    st = aes.decrypt(enc)
    st = st.decode('utf8')  # because utf8 is what everyone uses
    # ^^ decode error might be returned even when password is wrong
    # check if correctly decoded
    if not st.endswith(EXTRA_STR_2):
        return None
    else:
        return st[:-1 * len(EXTRA_STR_2)]


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
        try:
            newData = funcptr(key, data)
        except Exception:
            print_exc()
            newData = None  # handled sufficiently well now
        if newData is None:
            newData = data
            failed = True
            print_err('Failed processing %s' % file)
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


def key_32(key):
    if len(key) > 32:
        key = key[:32]
    else:
        key = key + ('0' * (32 - len(key)))
    return bytes(key, 'utf8')
