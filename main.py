#!/usr/python3
from sys import argv
import magic
import os,shutil,string

def checkImage(fl):

    f_lowername= fl.lower()
    imgTypes  = ["jpg","png","jpeg"]
    for imgtype in imgTypes:
        if "."+imgtype in f_lowername:
            return [True,fl]

    ext = "."+magic.from_file(fl,mime=True).split('/')[-1]
    
    for imgtype in imgTypes:
        if "."+imgtype in ext:
            print(ext)
            fpath = "/".join(fl.split("/")[:-1])+"/"
            fname = fl.split("/")[-1]
            finalNm=fpath+fname.replace(".","")+ext
            print(finalNm)
            shutil.move(fl,finalNm)
            return [True,finalNm]
    return [False,'assa']



def scanFiles(folder):

    names=[]

    with open("/home/vamshi/.actnames.txt",'r') as fl:
        for ln in fl:
            names.append(ln[:-1])

    imgFiles=[]

    for root, directories, filenames in os.walk(folder):
        for filename in filenames:
            if "9351" in filename or filename.startswith("gsd"):
                continue
            try:
                    
                    f=os.path.abspath(os.path.join(root,filename))
                    isValid,f = checkImage(f)
                    found = False
                    for nm in names:
                        if nm in f.split("/")[-1].lower():
                            found = True
                            break
                    

                    if isValid and not found:
                        #print(f)
                        fsz=os.stat(f).st_size
                        if fsz < 10240 or fsz > 6824000:
                            continue
                        imgFiles.append([f,fsz])
            except Exception as e:
                print(e)

    files = sorted(imgFiles,key=lambda x:x[1],reverse=True)

    #print(files)

    return files

def traverseFiles(files):

    for fl in files:
        print(fl)



def main():

    if len(argv) > 0:
        scanFolder = argv[1]
        print("Scanning Files in {scanFolder}".format(scanFolder=scanFolder))

        files = scanFiles(scanFolder)

        traverseFiles(files)


if __name__ == "__main__":
    main()