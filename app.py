import os
import requests
import time
import json
import magic
from getpass import getpass

def printLines():
    print("--------------------------------------------------------")

def printDesign(s):
    os.system('cls')
    
    printLines()
    print("\t\t\t"+s)
    printLines()

def isValidUsername(s):
    if(s != ""):
        if(len(s) >= 5):
            if(s.islower()):
                return True
    return False

def isValidFullname(s):
    if(s != ""):
        if(s.isalpha()):
                return True
    return False

def isValidPassword(s):
    if(s != ""):
        if(len(s) >= 8):
            for i in s:
                if((ord(i)>=65) and (ord(i) <= 90)):
                    return True
    return False

def login():
    printDesign("LOGIN")

    username = input("Enter Your Username  : ")
    password = getpass("Enter Your Password  : ")

    if(isValidUsername(username)):
        if(isValidPassword(password)):
            headers = {
                "accept": "application/json",
                "content-type": "application/x-www-form-urlencoded"
            }

            r = requests.post('http://127.0.0.1:8000/token', data= {
                "username" : username,
                "password" : password 
            }, headers=headers)
            
            j = r.json()
            if(("status_code" in j.keys()) and (j["status_code"] == 400)):
                printLines()
                print(j["detail"])
                printLines()
            else:
                return j["access_token"]

        else:
            printLines()
            print("INVALID PASSWORD")
            printLines()
    else:
        printLines()
        print("INVALID PASSWORD")
        printLines()

    time.sleep(1.5)
    main()

def signup():
    printDesign("SIGN UP")

    print("NOTE:")
    print("username: Minimum 5 characters long and should be in lowercase")
    print("password: Minimum 8 characters long and atleast one uppercase character")
    printLines()

    username = input("Enter Your Username  : ")
    fullname = input("Enter Your Fullname  : ")
    password = getpass("Enter Your Password  : ")
    repassword = getpass("Re-Type Your Password: ")

    if(isValidUsername(username)):
        if(isValidFullname(fullname)):
            if(isValidPassword(password)):
                if(password == repassword):
                    data = {
                        "username": username,
                        "fullname": fullname,
                        "password": password
                    }

                    headers = {
                        "accept": "application/json",
                        "content-type": "application/json"
                    }

                    r = requests.post('http://127.0.0.1:8000/signup', data=json.dumps(data), headers=headers)

                    j = r.json()
                    if(("status_code" in j.keys()) and (j["status_code"] == 400)):
                        printLines()
                        print(j["detail"])
                        printLines()
                    else:
                        printLines()
                        print("Account Successfully CREATED!!!")
                        printLines()

                        time.sleep(1.5)
                        main()

                else:
                    printLines()
                    print("PASSWORD AND RE_TYPE PASSWORDS SHOULD MATCH")
                    printLines()
            else:
                printLines()
                print("INVALID PASSWORD CHECK THE NOTE")
                printLines()
        else:
            printLines()
            print("INVALID FULLNAME")
            printLines()
    else:
        printLines()
        print("INVALID USERNAME CHECK THE NOTE")
        printLines()

    time.sleep(1.5)
    signup()

def uploadFile(token):
    printDesign("UPLOAD A FILE")

    filePath = input("ENTER THE PATH OF THE FILE THAT YOU WANT TO UPLOAD: ")

    if(os.path.exists(filePath)):
        fileName = filePath[filePath.rindex("\\")+1:]
        mime = magic.Magic(mime=True)
        x = mime.from_file(filePath)

        s = "Bearer " + token
        headers = {
            "accept": "application/json",
            "Authorization": s,
        }

        files = {
            "file" : (fileName, open(filePath, "rb"), x)
        }

        r = requests.post('http://127.0.0.1:8000/uploadfile', files=files, headers=headers)

        j = r.json()
        cd = "status_code"
        if((cd in j.keys()) and (j[cd] == 400)):
            printLines()
            print(j["detail"])
            printLines()
        else:
            printLines()
            print("FILE UPLOADED SUCCESSFULLY!!!")
            printLines()

            time.sleep(2)
            homepage(token)

    else:
        printLines()
        print("\tINVALID FILE PATH")
        printLines()

def getTheFiles(token):
    s = "Bearer " + token
    headers = {
        "accept": "application/json",
        "Authorization": s,
    }

    r = requests.get('http://127.0.0.1:8000/getfiles', headers=headers)

    return r.json()

def displayFile(token):
    printDesign("DISPLAY THE FILES")

    j = getTheFiles(token)

    c = 1

    print("\n")
    printLines()
    print("\t\t\tYOUR FILES")
    printLines()
    
    if(len(j["ownedfiles"]) > 0):
        for i in j["ownedfiles"].keys():
            print(str(c) + ". " + j["ownedfiles"][i])
            c = c + 1 
    else:
        print("\t\t\tNONE")

    printLines()

    print("\n")
    printLines()
    print("\t\tFILES SHARED WITH YOU")
    printLines()
    
    c = 1
    if(len(j["sharedfiles"]) > 0):
        for i in j["sharedfiles"].keys():
            print(str(c) + ". " + j["sharedfiles"][i])
            c = c + 1
    else:
        print("\t\t\tNONE")

    printLines()
    
    ch = input("Do You Want to go Back(Y/N): ")

    if((ch == "Y") or (ch == "y")):
        homepage(token)


def downloadFile(token):
    printDesign("DOWNLOAD A FILE")

    j = getTheFiles(token)

    c = 1
    d = {}

    print("\n")
    printLines()
    print("\t\t\tYOUR FILES")
    printLines()
    
    if(len(j["ownedfiles"]) > 0):
        for i in j["ownedfiles"].keys():
            print(str(c) + ". " + j["ownedfiles"][i])
            d[c] = [i, j["ownedfiles"][i]]
            c = c + 1 
    else:
        print("\t\t\tNONE")

    printLines()

    print("\n")
    printLines()
    print("\t\tFILES SHARED WITH YOU")
    printLines()
    
    if(len(j["sharedfiles"]) > 0):
        for i in j["sharedfiles"].keys():
            print(str(c) + ". " + j["sharedfiles"][i])
            d[c] = [i, j["sharedfiles"][i]]
            c = c + 1
    else:
        print("\t\t\tNONE")

    printLines()

    print("\n")
    
    num = int(input("Enter the File Number that you want to DOWNLOAD: "))
    
    if(num >= c):
        printLines()
        print("INVALID FILE NUMBER!!!")
        printLines()

        time.sleep(2)
        homepage(token)
    
    s = "Bearer " + token
        
    headers = {
        "accept": "*/*",
        "Authorization": s,
    }

    x = int(d[num][0])
    url = 'http://127.0.0.1:8000/downloadfile'+"?filesid="+str(x)

    r = requests.get(url, headers=headers)

    fileName = str(r.headers.get('content-disposition'))
    fileName = fileName[fileName.rindex(";")+12:-1]
    
    open("C:\\Users\\m_d_v\\Downloads\\"+fileName, "wb").write(r.content)

    printLines()
    print("FILE DOWNLOADED SUCCESSFULLY!!!")
    printLines()

    time.sleep(2)
    homepage(token)

def shareFile(token):
    printDesign("SHARE A FILE")

    j = getTheFiles(token)

    c = 1
    d = {}

    print("\n")
    printLines()
    print("\t\t\tYOUR FILES")
    printLines()
    
    if(len(j["ownedfiles"]) > 0):
        for i in j["ownedfiles"].keys():
            print(str(c) + ". " + j["ownedfiles"][i])
            d[c] = [i, j["ownedfiles"][i]]
            c = c + 1 
    else:
        print("\t\t\tNONE")

    printLines()

    print("\n")
    printLines()
    print("\t\tFILES SHARED WITH YOU")
    printLines()
    
    if(len(j["sharedfiles"]) > 0):
        for i in j["sharedfiles"].keys():
            print(str(c) + ". " + j["sharedfiles"][i])
            d[c] = [i, j["sharedfiles"][i]]
            c = c + 1
    else:
        print("\t\t\tNONE")

    printLines()

    print("\n")
    
    num = int(input("Enter the File Number that you want to SHARE: "))
    
    if(num >= c):
        printLines()
        print("INVALID FILE NUMBER!!!")
        printLines()

        time.sleep(2)
        homepage(token)
    
    t = int(input("Enter the Number of People You Want to share this with: "))

        
    s = "Bearer " + token
        
    headers = {
        "accept": "application/json",
        "Authorization": s,
    }

    c = 1
    for i in range(t):
        print("\n")
        name = input("Enter the username of Person-"+str(c)+": ")

        x = int(d[num][0])
        url = 'http://127.0.0.1:8000/sharefiles'+"?fileid="+str(x)+"&toUser="+str(name)
  
        r = requests.get(url, headers=headers)

        j = r.json()
    
        if(("status_code" in j.keys()) and (j["status_code"] == 400)):
            printLines()
            print(j["detail"])
            printLines()
        elif(("status_code" in j.keys()) and (j["status_code"] == 401)):
            printLines()
            print(j["detail"])
            printLines()
        elif(("status_code" in j.keys()) and (j["status_code"] == 401)):
            printLines()
            print(j["detail"])
            printLines()
        else:
            printLines()
            print("FILE SHARED SUCCESSFULLY!!!")
            printLines()

        c = c + 1

    time.sleep(2)
    homepage(token)


def renameFile(token):
    printDesign("RENAME A FILE")

    j = getTheFiles(token)

    c = 1
    d = {}

    print("\n")
    printLines()
    print("\t\t\tYOUR FILES")
    printLines()
    
    if(len(j["ownedfiles"]) > 0):
        for i in j["ownedfiles"].keys():
            print(str(c) + ". " + j["ownedfiles"][i])
            d[c] = [i, j["ownedfiles"][i]]
            c = c + 1 
    else:
        print("\t\t\tNONE")

    printLines()

    print("\n")
    printLines()
    print("\t\tFILES SHARED WITH YOU")
    printLines()
    
    if(len(j["sharedfiles"]) > 0):
        for i in j["sharedfiles"].keys():
            print(str(c) + ". " + j["sharedfiles"][i])
            d[c] = [i, j["sharedfiles"][i]]
            c = c + 1
    else:
        print("\t\t\tNONE")

    printLines()

    print("\n")
    
    num = int(input("Enter the File Number that you want to RENAME: "))
    
    if(num >= c):
        printLines()
        print("INVALID FILE NUMBER!!!")
        printLines()

        time.sleep(2)
        homepage(token)
    
    newName = input("Enter the NEW NAME for the file: ")
    
    s = "Bearer " + token
        
    headers = {
        "accept": "application/json",
        "Authorization": s,
    }

    x = int(d[num][0])
    url = 'http://127.0.0.1:8000/renamefile'+"?fileid="+str(x)+"&newName="+str(newName)

    r = requests.get(url, headers=headers)

    j = r.json()

    if(("status_code" in j.keys()) and (j["status_code"] == 400)):
        printLines()
        print(j["detail"])
        printLines()
    else:
        printLines()
        print("FILE RENAMED SUCCESSFULLY!!!")
        printLines()


    time.sleep(2)
    homepage(token)

def deleteFile(token):
    printDesign("DELETE A FILE")

    j = getTheFiles(token)

    c = 1
    d = {}

    print("\n")
    printLines()
    print("\t\t\tYOUR FILES")
    printLines()
    
    if(len(j["ownedfiles"]) > 0):
        for i in j["ownedfiles"].keys():
            print(str(c) + ". " + j["ownedfiles"][i])
            d[c] = [i, j["ownedfiles"][i]]
            c = c + 1 
    else:
        print("\t\t\tNONE")

    printLines()

    print("\n")
    printLines()
    print("\t\tFILES SHARED WITH YOU")
    printLines()
    
    if(len(j["sharedfiles"]) > 0):
        for i in j["sharedfiles"].keys():
            print(str(c) + ". " + j["sharedfiles"][i])
            d[c] = [i, j["sharedfiles"][i]]
            c = c + 1
    else:
        print("\t\t\tNONE")

    printLines()

    print("\n")
    
    num = int(input("Enter the File Number that you want to DELETE: "))
    
    if(num >= c):
        printLines()
        print("INVALID FILE NUMBER!!!")
        printLines()

        time.sleep(2)
        homepage(token)
    
    s = "Bearer " + token
        
    headers = {
        "accept": "application/json",
        "Authorization": s,
    }

    x = int(d[num][0])
    url = 'http://127.0.0.1:8000/deletefile'+"?fileid="+str(x)

    r = requests.get(url, headers=headers)

    j = r.json()

    if(("status_code" in j.keys()) and (j["status_code"] == 400)):
        printLines()
        print(j["detail"])
        printLines()
    else:
        printLines()
        print("FILE DELETED SUCCESSFULLY!!!")
        printLines()

    time.sleep(2)
    homepage(token)

def homepage(token):
    s = "Bearer " + token
    headers = {
        "accept": "application/json",
        "Authorization": s,
    }

    r = requests.get('http://127.0.0.1:8000/users/me', headers=headers)

    j = r.json()

    printDesign("CLOUDY - " + str(j["fullname"]))

    print("1. UPLOAD A FILE")
    print("2. DISPLAY THE FILES STORED IN CLOUD")
    print("3. DOWNLOAD A FILE")
    print("4. SHARE A FILE")
    print("5. RENAME A FILE")
    print("6. DELETE A FILE")
    print("7. EXIT")

    printLines()

    ch = int(input("\nEnter Your Choice: "))

    if(ch == 1):
        uploadFile(token)
    elif(ch == 2):
        displayFile(token)
    elif(ch == 3):
        downloadFile(token)
    elif(ch == 4):
        shareFile(token)
    elif(ch == 5):
        renameFile(token)
    elif(ch == 6):
        deleteFile(token)
    elif(ch == 7):
        quit()
    else:
        printLines()
        print("INVALID CHOICE!!!")
        printLines()


def main():
    printDesign("CLOUDY")

    print("1. LOGIN")
    print("2. SIGN UP")

    printLines()

    ch = int(input("\nEnter Your Choice: "))

    if(ch == 1):
        token = login()
        
        homepage(token)

    elif(ch == 2):
        signup()
    else:
        printLines()
        print("INVALID CHOICE!!!")
        printLines()
        
main()
