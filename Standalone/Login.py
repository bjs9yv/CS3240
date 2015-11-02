__author__ = 'adminuser'
import RSA
import os
import getpass


USERNAME="bnc4vk"
PASSWORD="password"

print("** Launching standalone application...\n")

# lOGIN
check = True
while check:
    usr = input("Enter SecureContact username: ")
    if usr == USERNAME: # TODO: this will have to check the database online 
        check = False
        while True:
            pswd = getpass.getpass()
            if pswd == PASSWORD:
                print('\n')
                break
    else:
        print("Username not recognized, please try again")

# POST LOGIN PROCEDURE
if "PrivateKey.txt" not in os.listdir(os.getcwd()): # TODO change this to search sub directory where keys are stored
    print("** It looks like this is your first time! Generating key pair...\n")
    RSA.gen_keys()
    print("** Successfully created public/private key pair...\n")
    # TODO: upload PublicKey.txt to db
    # print("** Uploading public key to SecureContact site...\n")

print("Available reports:")

reports = 5 # TODO: pull reports available to this username from db

for i in range(5):
    print("Report [" + str(i) + "]:")

command_list = ['DOWNLOAD', '...', '..', '.']

for item in command_list:
    print(item)

command = input("Choose command")

if command == "DOWNLOAD":
    file = input("Choose file to download")
