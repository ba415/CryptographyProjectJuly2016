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
#from __future__ import print_function

# === Init logging level ==========================================================================
# For more detailed logging update logging.INFO to logging.DEBUG
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# User Key Generation Info
# TODO: Put in a property file
user1 = {'name_real': 'meman',
         'name_email': 'test@test.edu',
         'expire_date': '2017-04-01',
         'key_type': 'RSA',
         'key_length': 2048,
         'key_usage': '',
         'subkey_type': 'RSA',
         'subkey_length': 2048,
         'subkey_usage': 'encrypt,sign,auth',
         'passphrase': 'foobar'}

class gb_cloud():
    # class functions
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()  # creates local web server
        self.drive = GoogleDrive(gauth)
        
    def upload ( self, localFile, cloudFilePath,key_dir,key_id ):
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

    def downloadPublicKey(self, cloudKeyFile, localKeyFile):
        # download from the cloud to your local user space
        try:
            logger.info('Download of public keys Starting')
            self.drive.downloadFile(cloudKeyFile, localKeyFile)
            logger.info('Download Complete')
        except:
            logger.error('Download public keys Failed, Unexpected Error: s%', sys.exc_info()[0])
            raise

    def gen_keys(self, keydir, userInput):
        gpg = gnupg.GPG(gnupghome=keydir, gpgbinary='/usr/local/bin/gpg')

        user_input = gpg.gen_key_input(**userInput)
        logger.info('User Key Input: %s', user_input)

        user_key = gpg.gen_key(user_input)
        logger.info('User Key: %s', user_key)

        return user_key

    def export_keys(self, keydir, user_key):
        gpg = gnupg.GPG(gnupghome=keydir, gpgbinary='/usr/local/bin/gpg')

        ascii_public_keys = gpg.export_keys(user_key)
        ascii_private_keys = gpg.export_keys(user_key, True)

        with open('public_keyfile.asc', 'w') as f_pub:
            f_pub.write(ascii_public_keys)
    
        with open('private_keyfile.asc', 'w') as f_pri:
            f_pri.write(ascii_private_keys)
        
    def import_pub_key(self, keydir, pubkeyfile):
        gpg = gnupg.GPG(gnupghome=keydir, gpgbinary='/usr/local/bin/gpg')

        try:
            key_data = open(pubkeyfile).read()
            import_result = gpg.import_keys(key_data)
            logger.info('Import Key: %s', import_result.results)
            # List keys to ensure it was imported
            logger.info('Public Keys: %s\n', gpg.list_keys())
        except:
            logger.error('Import Key Failed, Unexpected Error: s%', sys.exc_info()[0])
            raise

    def list_keys(self, keydir):
        gpg = gnupg.GPG(gnupghome=keydir, gpgbinary='/usr/local/bin/gpg')

        public_keys = gpg.list_keys()
        logger.info('Public Keys: %s\n', public_keys)

        private_keys = gpg.list_keys(True)
        logger.info('Private Keys: %s\n', private_keys)

    # To encrypt a file - need to know the fingerprint_id of the user
    def encrypt_file(self, input_file, keydir, key):
        gpg = gnupg.GPG(gnupghome=keydir, gpgbinary='/usr/local/bin/gpg')   
        encrypted_file = input_file + '.pgp'
        
        # Open input file
        file_stream = open(input_file, 'rb')
        enc_ascii_data = gpg.encrypt_file(file_stream, str(key), output=encrypted_file)
        file_stream.close()
        return encrypted_file

    def decrypt_file(self, encrypted_file, keydir, key):
       
        gpg = gnupg.GPG(gnupghome=keydir, gpgbinary='/usr/local/bin/gpg')   
        decrypted_file = 'decrypted_file'
        
        # Open input file     
        with open(encrypted_file, 'rb') as f:
            status = gpg.decrypt_file(f, passphrase=user1.passphrase, output=decrypted_file)

            print 'ok: ', status.ok
            print 'status: ', status.status
            print 'stderr: ', status.stderr
            
        return decrypted_file

# Main
def main(argv):
    # create object handle to test functions
    handle = gb_cloud()

    parser = argparse.ArgumentParser(description='Encryption Application for tranferring files via Google Drive')
    parser.add_argument("-u", "--upload", action="store_true", help='Upload file to Google drive')
    parser.add_argument("-d", "--download", action="store_true", help='Download file from Google drive')
    parser.add_argument("file", help='File to upload or download')
    parser.add_argument("clientId1", help='client1 identifier e.g. client1')
    parser.add_argument("clientId2", help='client2 identifier e.g. client2')
    args = parser.parse_args()

    # Get file name
    fn = os.path.basename(args.file)
    logger.debug("filename -> %s", fn)
    
    # Get your client id 
    clientId1 = os.path.basename(args.clientId1)
    logger.debug("ClientId -> %s", clientId1)
    
    # Get other client id 
    clientId2 = os.path.basename(args.clientId2)
    logger.debug("ClientId -> %s", clientId2)

    #Upload path - Remove hard-coded path
    upload_path = 'CryptoProjectDrive/' + fn + '.pgp'
    logger.debug("upload_path -> %s", upload_path)

    #Download path - Remove hard-coded path
    download_path = 'CryptoProjectDrive/' + fn
    logger.debug("download_path -> %s", download_path)

    # Generate and export keys
    # Commenting out for now...generating keys takes too long 
    keysdir = 'keys'

    key_id = handle.gen_keys(keysdir, user1)
    logger.debug("Key ID: %s", key_id)
    handle.export_keys(keysdir, str(key_id))
    handle.uploadPublicKey(clientId1)

    if args.upload and os.path.isfile(args.file):
        logger.debug('Upload File to Cloud ' + fn)
        #Encrypt and Upload file
        enc_filename = handle.upload(fn, upload_path, 'keys', key_id)
        
    elif args.download and os.path.isfile(args.file):
        logger.debug('Download\n')
        #Download file
        handle.download(args.file, download_path)
       
if __name__ == '__main__':
    main(sys.argv)
