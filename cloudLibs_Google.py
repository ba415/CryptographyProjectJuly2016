'''
Created on Jul 16, 2016
@author: Asia LaBrie
@description: Create upload, download, auth and other functions for connecting and using to the google drive api
'''
import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class gb_cloud():
     
    #class functions
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth() #creates local web server
        self.drive = GoogleDrive(gauth)
        #TODO - set directory path!
    
    def disconnect(self):
        print 'disconnect to google drive'
        
    def getParentFolder(self,gbPath):
        folderId = 0
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            if file1['title'] == gbPath:
                folderId = file1['id']
                
        if (folderId == 0): 
            #create new folder
            file1 = self.drive.CreateFile({'title': gbPath, "mimeType": "application/vnd.google-apps.folder"})
            file1.Upload()
            folderId = file1['id']
            
        return folderId
    
    def upload(self,folder,filename):
        #filename and filepath, if filepath is empty use current directory
        folder_id = self.getParentFolder(folder)
        file2Upload = self.drive.CreateFile({'title': filename, "parents":  [{"kind": "drive#fileLink","id": folder_id}] })
        file2Upload.SetContentFile(filename)
        file2Upload.Upload()
        
    #get file id for file to download
    def getFile(self, filename):
        fileId = 0
        # Auto-iterate through all files in the root folder.
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        
        for file1 in file_list:
            print 'title: %s, id: %s' % (file1['title'], file1['id'])
            if (file1['title'] ==  filename):
                fileId = file1['id']
        
        return fileId 
            
    #Get file from google drive
    def download(self,folder,filename):
        fileId = self.getFile(filename)
        file2Download = self.drive.CreateFile({'id': fileId })
        file2Download.GetContentFile(filename)


def main(argv):    
    #create object handle to test functions
    handle = gb_cloud()
    handle.upload('test2','moon.jpg')
    handle.download('test2','moon.jpg')   
   

if __name__ == '__main__':
        main(sys.argv)