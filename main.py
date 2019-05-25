#!/usr/python3
from sys import argv
import magic
import os,shutil,string,time
from googleNamer import googleName
from threading import Thread,active_count


names=[]

def checkImage(fl):

    f_lowername= fl.lower()
    imgTypes  = ["jpg","png","jpeg"]
    for imgtype in imgTypes:
        if "."+imgtype in f_lowername:
            return [True,fl]

    ext = "."+magic.from_file(fl,mime=True).split('/')[-1]
    
    for imgtype in imgTypes:
        if "."+imgtype in ext:
            fpath = "/".join(fl.split("/")[:-1])+"/"
            fname = fl.split("/")[-1]
            finalNm=fpath+fname.replace(".","")+ext
            shutil.move(fl,finalNm)
            return [True,finalNm]
    return [False,'assa']



def scanFiles(folder):
    global names
    names=[]

    with open("/home/vamshi/.actnames.txt",'r') as fl:
        for ln in fl:
            names.append(ln[:-1])

    imgFiles=[]

    for root, directories, filenames in os.walk(folder):
        for filename in filenames:
            if "9351" in filename or filename.startswith("gsd") or filename.startswith("ugsd"):
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

def delay(sz):    
    
    sl=0
    if sz <= 2000:
        sl=1
    elif sz > 2000 and sz <= 5000:
        sl=1.45
    elif sz > 5000 and sz <= 10000:
        sl=2.0
    elif sz> 10000 and sz<=15000:
        sl=2.65
    elif sz > 15000 and sz<30000:
        sl=3.0
    else:
        sl=3.5

    print(sl)
    time.sleep(sl)
    os.system("killall pqiv")



def displayImage(img):
    fl,sz= img
    os.system("pqiv -c -f '"+fl+"' &")
    delay(sz)



def traverseFiles(files):

    for fl in files:
        print(fl)
        displayImage(fl)
        ch=input("Enter y('') or n(*):")
        if not ch == "":
            Thread(target=handleName,args=(fl[0],ch,)).start()
            if active_count() > 10:
                time.sleep(5)
        else:
            ch = input("Press enter to confirm:")
            if ch == "":
                os.remove(fl[0])

def handleName(fl,partnm):
    gname = googleName(fl).lower()
    if "" == gname:
        return ''
    print("gname:"+gname)

    found = 0
    for nm in names:
        try:
            if nm in gname and found == 0:
                found = 1
                fpath = "/".join(fl.split("/")[:-1])+"/"
                finalNm=fpath+"gsd"+gname.replace(".","")+partnm+".jpg"
                print(finalNm)
                shutil.move(fl,finalNm)
                return ''
        except Exception as e:
            print("renaming in handleName:"+e)

    if found == 0:
        fpath = "/".join(fl.split("/")[:-1])+"/"
        fname = fl.split("/")[-1].replace(" ","_")
        finalNm=fpath+"ugsd"+fname.replace(".","")+partnm+".jpg"
        
        shutil.move(fl,finalNm)

def main():

    if len(argv) > 0:
        scanFolder = argv[1]
        print("Scanning Files in {scanFolder}".format(scanFolder=scanFolder))

        files = scanFiles(scanFolder)

        traverseFiles(files)


if __name__ == "__main__":
    main()