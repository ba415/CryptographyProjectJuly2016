'''
Created on Jul 16, 2016
@author: Asia LaBrie
@description: Create upload, download, auth and other functions for connecting and using to the google drive api
'''
import sys
from pydrive.auth import GoogleAuth
#For walking the file directory structure
from pydrive_ex.drive import GoogleDrive 

class gb_cloud():
     
    #class functions
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth() #creates local web server
        self.drive = GoogleDrive(gauth)       
        
    def upload(self,localFilePath, cloudFilePath):
        #upload from the local user space to the google cloud
        try:
            print 'Upload Starting'
            self.drive.uploadFile(cloudFilePath, localFilePath)
            print 'Upload Complete ' 
        except:
            print 'Upload Failed, Unexpected Error:', sys.exc_info()[0]
            raise   
            
    def download(self,cloudFilePath,localFilePath):
        #download from the cloud to your local user space
        try:
            print 'Download Starting'
            self.drive.downloadFile(cloudFilePath, localFilePath)
            print 'Download Complete ' 
        except:
            print 'Download Failed, Unexpected Error:', sys.exc_info()[0]
            raise
        
    def putPublicKey(self,localKeyFile, cloudKeyFile):
        #upload from the local user space to the google cloud
        try:
            print 'Upload of public keys Starting'
            self.drive.uploadFile(cloudKeyFile, localKeyFile)
            print 'Upload Complete ' 
        except:
            print 'Upload of public keys Failed, Unexpected Error:', sys.exc_info()[0]
            raise   
            
    def getPublicKey(self,cloudKeyFile,localKeyFile):
        #download from the cloud to your local user space
        try:
            print 'Download of public keys Starting'
            self.drive.downloadFile(cloudKeyFile, localKeyFile)
            print 'Download Complete ' 
        except:
            print 'Download public keys Failed, Unexpected Error:', sys.exc_info()[0]
            raise    
        

def main(argv):    
    #create object handle to test functions
    handle = gb_cloud()
    handle.upload('upload/CryptographyCloudProject-draft.pptx','CryptoProjectDrive/CryptographyCloudProject-draft.pptx')
    #handle.download('CryptoProjectDrive/moon1.jpg','download/moon1.jpg')   
   

if __name__ == '__main__':
        main(sys.argv)