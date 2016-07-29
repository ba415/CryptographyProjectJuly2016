'''
@author: 
@description: Create upload, download, auth and other functions for connecting and using to the google drive api
'''
import os
import sys
import logging
import argparse
import gnupg

from pydrive.auth import GoogleAuth
# For walking the file directory structure
from pydrive_ex.drive import GoogleDrive

# === Init logging level ==========================================================================
# For more detailed logging update logging.INFO to logging.DEBUG
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define gpgbinary location
gpgbinary_path = '/usr/bin/gpg'

# User Key Generation Info
# TODO: Put in a property file
myuser = {'name_real': 'bekim',
         'name_email': 'test@test.edu',
         'expire_date': '2017-04-01',
         'key_type': 'RSA',
         'key_length': 2048,
         'key_usage': '',
         'subkey_type': 'RSA',
         'subkey_length': 2048,
         'subkey_usage': 'encrypt,sign,auth',
         'passphrase': ''}

class gb_cloud():
    # class functions
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()  # creates local web server
        self.drive = GoogleDrive(gauth)
        
    def upload ( self, localFile, cloudFilePath, key_dir, key_id ):
        # upload from the local user space to the google cloud
        try:
            encryted_filename = self.encrypt_file(localFile, key_dir, key_id)
            logger.info('Upload Starting for ' + encryted_filename)
            self.drive.uploadFile(cloudFilePath, encryted_filename)
            logger.info('Upload Complete')
            return encryted_filename
        except:
            logger.error('Upload Failed, Unexpected Error: s%', sys.exc_info()[0])
            raise

    def download(self, cloudFilePath, localFilePath):
        # download from the cloud to your local user space
        try:
            logger.info('Download Starting')
            self.drive.downloadFile(cloudFilePath, localFilePath)
            logger.info('Download Complete ')
        except:
            logger.error('Download Failed, Unexpected Error: %s', sys.exc_info()[0])
            raise

    def uploadPublicKey(self, clientId):
        # upload from the local user space to the google cloud
        try:
            logger.info('Upload of public keys Starting')
            upload_publickey = 'CryptoProjectDrive/securityObjects/' + clientId + '_public_keyfile.asc'
            self.drive.uploadFile(upload_publickey, 'public_keyfile.asc')
            logger.info('Upload Complete')
        except:
            logger.error('Upload of public keys Failed, Unexpected Error: s%', sys.exc_info()[0])
            raise

    def downloadPublicKey(self, clientId):
        # download from the cloud to your local user space
	localKeyFile = ''
        try:
            logger.info('Download of public keys Starting')
            cloudKeyFile = 'CryptoProjectDrive/securityObjects/' + clientId + '_public_keyfile.asc'
            localKeyFile = clientId + '_public_keyfile.asc'
            self.drive.downloadFile(cloudKeyFile, localKeyFile)
            logger.info('Download Complete')
        except:
            logger.error('Download public keys Failed, Unexpected Error: s%', sys.exc_info()[0])
            raise

        return localKeyFile

    def gen_keys(self, keydir, userInput):
        gpg = gnupg.GPG(gnupghome=keydir, gpgbinary=gpgbinary_path, verbose=False)

        user_input = gpg.gen_key_input(**userInput)
        logger.info('User Key Input: %s', user_input)

        user_key = gpg.gen_key(user_input)
        logger.info('User Key: %s', user_key)

        return user_key

    def export_keys(self, keydir, user_key):
        gpg = gnupg.GPG(gnupghome=keydir, gpgbinary=gpgbinary_path, verbose=False)

        ascii_public_keys = gpg.export_keys(user_key)
        ascii_private_keys = gpg.export_keys(user_key, True)

        with open('public_keyfile.asc', 'w') as f_pub:
            f_pub.write(ascii_public_keys)
    
        with open('private_keyfile.asc', 'w') as f_pri:
            f_pri.write(ascii_private_keys)
        
    def import_pub_key(self, keydir, pubkeyfile):
        gpg = gnupg.GPG(gnupghome=keydir, gpgbinary=gpgbinary_path, verbose=False)

        try:
            key_data = open(pubkeyfile).read()
            import_result = gpg.import_keys(key_data)
            logger.info('Import Key: %s\n', import_result.results)
            # List keys to ensure it was imported
            logger.info('Public Keys: %s\n', gpg.list_keys())
        except:
            logger.error('Import Key Failed, Unexpected Error: s%', sys.exc_info()[0])
            raise

    def list_keys(self, keydir):
        gpg = gnupg.GPG(gnupghome=keydir, gpgbinary=gpgbinary_path, verbose=False)

        public_keys = gpg.list_keys()
        logger.info('Public Keys: %s\n', public_keys)

        private_keys = gpg.list_keys(True)
        logger.info('Private Keys: %s\n', private_keys)

    # To encrypt a file - need to know the fingerprint_id of the user
    def encrypt_file(self, input_file, keydir, key):
        gpg = gnupg.GPG(gnupghome=keydir, gpgbinary=gpgbinary_path, verbose=False)
        encrypted_file = input_file + '.pgp'
        
        # Open input file
        file_stream = open(input_file, 'rb')
        enc_ascii_data = gpg.encrypt_file(file_stream, str(key), output=encrypted_file)
        file_stream.close()
        return encrypted_file

    def decrypt_file(self, encrypted_file, keydir, key):
       
        gpg = gnupg.GPG(gnupghome=keydir, gpgbinary=gpgbinary_path, verbose=False)
        filename, file_extension = os.path.splittext(encrypted_file)
	logger.debug("File name: %s, File extension: %s", (filename, file_extension))
	decrypted_file = filename
        
        # Open input file     
        with open(encrypted_file, 'rb') as f:
            status = gpg.decrypt_file(f, passphrase=myuser.passphrase, output=decrypted_file)

            logger.info('ok: %s', status.ok)
            logger.info('status: %s', status.status)
            logger.info('stderr: %s', status.stderr)
            
        return decrypted_file

# Main
def main(argv):
    
    # create object handle to test functions
    handle = gb_cloud()
    # Key Dir 
    keysdir = 'keys'

    menu = {}
    menu['1'] = "Generate Private and Public Keys`"
    menu['2'] = "View Private and Public Keys on local keyring"
    menu['3'] = "Export Private and Public Keys"
    menu['4'] = "Upload Public Key to Google Cloud"
    menu['5'] = "Import Public Key from Google Cloud"
    menu['6'] = "Encrypt and Upload File to Google Cloud"
    menu['7'] = "Download and Decrypt File from Google Cloud"
    menu['8'] = "Exit"
    while True:
        options = menu.keys()
        options.sort()
        for entry in options:
            logger.info(" %s: %s" % (entry, menu[entry]))

        logger.info(" Please Select: ")
        selection = raw_input()
        if selection == '1':
            input_passphrase = raw_input("Enter Pass Phrase to Generate Keys: ")
            # TODO - remove this line
            logger.debug("Input Pass Phrase: %s", input_passphrase)
            myuser['passphrase'] = input_passphrase
            key_id = handle.gen_keys(keysdir, myuser)
            logger.debug("Key ID Generated: %s", key_id)
        elif selection == '2':
            handle.list_keys(keysdir)
        elif selection == '3':
            input_key = raw_input("Enter the Key ID to export: ")
            logger.debug("Key ID entered: %s", input_key)
            handle.export_keys(keysdir, str(input_key))
        elif selection == '4':
            handle.uploadPublicKey(myuser['name_real'])
        elif selection == '5':
            pub_user_to_import = raw_input("Enter ID of user to import public key: ")
            logger.debug("Public Import User ID: %s", pub_user_to_import)
            # Download and import public key from cloud
	    public_key_file_from_cloud = handle.downloadPublicKey(pub_user_to_import)
            logger.debug("Public Key File from Cloud: %s", public_key_file_from_cloud)
            handle.import_pub_key(keysdir,public_key_file_from_cloud)
        elif selection == '6':
            logger.debug("Encrypt and Upload File to Cloud\n")
            # Encrypt file
            fn_path = raw_input("Enter file to upload: ")
            # Get file name
            fn = os.path.basename(fn_path)
            logger.debug("filename -> %s", fn)
            enc_key = raw_input("Enter Key ID to encrypt with: ")
            logger.debug("Encrypt Key ID entered: %s", enc_key)
            # Upload path - Remove hard-coded path
            upload_path = 'CryptoProjectDrive/' + fn + '.pgp'
            logger.debug("upload_path -> %s", upload_path)
            # Encrypt and Upload file
            enc_filename = handle.upload(fn, upload_path, keysdir, enc_key)
        elif selection == '7':
            logger.debug("Download and Decrypt from Cloud")
            fd_path = raw_input("Enter file to download: ")
            fd = os.path.basename(fd_path)
            logger.debug("filename -> %s", fd)
	    dec_passphrase = raw_input("Enter Pass Phrase To Decrypt File: ")
            # TODO - Remove this line
            logger.debug("Decrypt Pass Phrase: %s", dec_passphrase)
            myuser.passphrase = dec_passphrase
            # Download path - Remove hard-coded path
            download_path = 'CryptoProjectDrive/' + fd
            logger.debug("download_path -> %s", download_path)
	    # Download and Decrypt file
            handle.download(fd, download_path)
        elif selection == '8':
            break
        else:
            logger.info("Unknown Option Selected!\n") 

        
if __name__ == '__main__':
    main(sys.argv)
