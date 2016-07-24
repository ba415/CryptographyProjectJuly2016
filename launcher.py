'''
Created on Jul 23, 2016
@author: Asia LaBrie
@description: GUI for cloud libs
'''

from Tkinter import *
import cloudLibs_Google

class execute(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   
        
        self.parent = parent
        self.parent.title("Encrypt and Decrypt Wizard")
        
        Label(self.parent, text="File Src: ").grid(row=1, pady=10, padx=5)
        Label(self.parent, text="File Dest:").grid(row=2, pady=5, padx=5)

        self.src = Entry(self.parent)
        self.dest = Entry(self.parent)
        self.src.grid(row=1, column=1, padx=5)
        self.dest.grid(row=2, column=1, padx=5)

        Button(self.parent, text='Upload', command=self.upload).grid(row=5, column=0, pady=5, padx=10)
        Button(self.parent, text='Download', command=self.download).grid(row=5, column=1, pady=5, padx=10)
        Button(self.parent, text='Quit', command=self.parent.quit).grid(row=6, columnspan=2, pady=10)

    def upload(self):
        src = self.src.get()
        dest = self.src.get()
        print("Upload: File Src: %s\nFile Dest: %s" % (src, dest))
        if ( src and dest ):  
            handle = cloudLibs_Google.gb_cloud()
            handle.upload(src,dest)
        else:
            print 'Error Uploading File src or dest not provided'

    def download(self):
        src = self.src.get()
        dest = self.src.get()
        print("Download: File Src: %s\nFile Dest: %s" % (src, dest))
        if ( src and dest ): 
            handle = cloudLibs_Google.gb_cloud()
            handle.download(src,dest)
        else:
            print 'Error Downloading File src or dest not provided'

def main():
    root = Tk()
    execute(root)
    root.mainloop()
    


if __name__ == '__main__':
    main()