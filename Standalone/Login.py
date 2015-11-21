__author__ = 'adminuser'
from Crypto.PublicKey import RSA
import KeyCheck
import os
import getpass
import requests
import re
from Crypto import Random

print("*********************************************************************************")
print("**                                                                             **")
print("**    .oooooo..o                                                               **")
print("**   d8P'    `Y8                                                               **")
print("**   Y88bo.       .ooooo.   .ooooo.  oooo  oooo  oooo d8b  .ooooo.             **")
print("**    `'Y8888o.  d88' `88b d88' `'Y8 `888  `888  `888''8P d88' `88b            **")
print("**        `'Y88b 888ooo888 888        888   888   888     888ooo888            **")
print("**   oo     .d8P 888    .o 888   .o8  888   888   888     888    .o            **")
print("**   8''88888P'  `Y8bod8P' `Y8bod8P'  `V88V'V8P' d888b    `Y8bod8P'            **")
print("**                                                                             **")
print("**                                                                             **")                                                               
print("**     .oooooo.                             .                           .      **")
print("**    d8P'  `Y8b                          .o8                         .o8      **")
print("**   888           .ooooo.  ooo. .oo.   .o888oo  .oooo.    .ooooo.  .o888oo    **")
print("**   888          d88' `88b `888P'Y88b    888   `P  )88b  d88' `'Y8   888      **")
print("**   888          888   888  888   888    888    .oP'888  888         888      **")
print("**   `88b    ooo  888   888  888   888    888 . d8(  888  888   .o8   888 .    **")
print("**    `Y8bood8P'  `Y8bod8P' o888o o888o   '888' `Y888''8o `Y8bod8P'   '888'    **")
print("**                                                                             **")
print("**                                                     by Team Sixteen         **")
print("**                                                                             **")
print("*********************************************************************************")
print("*********************** Launching standalone application...**********************")

# lOGIN
user = ""
while True:
    user = input("Enter SecureContact username: ")
    pswd = getpass.getpass()
    passdic = {'username':user,'password':pswd}
    response = requests.get('http://t16-heroku-app.herokuapp.com/check_login/', params=passdic)
    if response.json()['valid']:
        print("** Login Successfull **\n")
        break
    else:
        print("Username or password not recognized, please try again")
        
# POST LOGIN PROCEDURE
if "PrivateKey.txt" not in os.listdir(os.getcwd()): # TODO change this to search sub directory where keys are stored
    print("** It looks like this is your first time! Generating key pair...\n")
    KeyCheck.gen_keys()
    print("** Successfully created public/private key pair...\n")
    # TODO: upload PublicKey.txt to db
    # print("** Uploading public key to SecureContact site...\n")

print("Welcome to the Secure Contact server " + str(user) + ".")
while True:
    print("\nHere is the list of possible commands: \n")
    commands = {1 : 'VIEW AVAILABLE REPORTS', 2 : 'UPLOAD REPORT', 3: 'QUIT'}
    for item in commands:
        print("\t" + str(item) + ": " + commands[item])
    cmd_choice = input("\nWhat would you like to do? ")    
    if cmd_choice.upper() == commands[1] or cmd_choice == '1':
        print("\nPulling reports from secured server...\n")
        reports = {1 : 'file.txt', 2 : 'trapqueen.wapp', 3 : 'wahoo.wa', 4 : 'hortonhearsa.hoo'}# TODO: pull reports available to this username from db
        reports_list = []
        reports_index = []
        for item in reports:
            reports_list.append(reports[item])
            reports_index.append(str(item))
        for item in reports:
            print("\tReport[" + str(item) + "]: " + reports[item])
        while True:
            choice = input("\nSelect a file to download, or return to the command menu: ")
            if choice in reports_index:
                print("\tDownloading " + reports[int(choice)] + "...")
            elif choice in reports_list:
                print("\tDownloading " + choice + "...")                
            elif re.match(r'((M|m)enu)|((R|r)eturn)|((Q|q)(.*))', choice):
                break
            else:
                print("\tError in selection: Invalid action [-" + choice + "-]")
    elif cmd_choice.upper() == commands[2] or cmd_choice == '2':
        file_name = input("\nPlease specify the file to upload: ")
        file_path = ""
        root_check = False
        for item in os.listdir(os.getcwd()):
            if item == file_name:
                root_check = True
                break
        if not root_check:
            print("\nThe requested file is not within the current working directory.")
            file_path = input("Please specifiy the file path or enter 'Unknown': ")
            if file_path == 'Unknown':
                check = False
                multiple = False
                file_paths = []
                for root, dirs, files in os.walk('/home'):
                    for f in files:
                        if f == file_name:
                            file_path = root + '/'
                            file_paths.append(file_path)
                            if not check:
                                check = True
                            else:
                                multiple = True
                if multiple:
                    print("Multiple files were found with the given filename [" + file_name + "]:")
                    cntr = 1
                    file_dict = {}
                    for f in file_paths:
                        print("\t" + str(cntr) + ": " + f + file_name)
                        cntr += 1
                        file_dict[cntr] = f
                    file_choice = input("Choice the file to upload: ")
                    for f in file_dict:
                        if str(f) == file_choice or file_dict[f] + file_name == file_choice:
                            file_path = file_dict[f]
                            break
        try:
            f = open(file_path + file_name, "rb")
            file_contents = f.read()
            encrypt = input("Would you like to encrypt the file before uploading? ")
            if re.match(r'(Y|y)(.*)', encrypt):
                #RSA....
                public_key = ""
                with open("PublicKey.txt", "r") as pk:
                    public_key = pk.read()
                key = RSA.importKey(public_key)
                encrypted_file = key.encrypt(file_contents, 32)
                print(encrypted_file)
                print("Uploading encrypting file...")
            else:
                #Upload
                print("Uploading file...")
            f.close()
        except FileNotFoundError:
            print("Error: Invalid file name " + file_path + file_name)
    elif cmd_choice.upper() == commands[3] or cmd_choice == '3':
        break
    else:
        print("\tError in selection: Invalid action [-" + cmd_choice + "-]")

