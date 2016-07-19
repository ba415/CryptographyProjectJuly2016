'''
Created on Jul 16, 2016
@author: Asia LaBrie
@description: Create upload, download, auth and other functions for connecting and using to the google drive api
'''
import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
#For walking the file directory structure
from pydrive_ex.drive import GoogleDrive 

class gb_cloud():
     
    #class functions
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth() #creates local web server
        self.drive = GoogleDrive(gauth)       
    
    def disconnect(self):
        print 'disconnect to google drive'
        
    def upload(self,localFile, cloudFile):
        try:
            print 'Upload Starting'
            self.drive.uploadFile(cloudFile, localFile)
            print 'Upload Complete ' 
        except:
            print 'Upload Failed'
            print 'Unexpected Error:', sys.exc_info()[0]
            raise   
            
    #Get file from google drive
    def download(self,cloudFile,localFile):
        try:
            print 'Download Starting'
            self.drive.downloadFile(cloudFile, localFile)
            print 'Download Complete ' 
        except:
            print 'Download Failed'
            print 'Unexpected Error:', sys.exc_info()[0]
            raise

def main(argv):    
    #create object handle to test functions
    handle = gb_cloud()
    handle.upload('upload/moonTest.jpg','test2/images/moon123.jpg')
    handle.download('test2/images/moon.jpg','download/moonDL.jpg')   
   

if __name__ == '__main__':
        main(sys.argv)