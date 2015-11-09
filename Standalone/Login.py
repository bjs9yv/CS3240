__author__ = 'adminuser'
import RSA
import os
import getpass


USERNAME="bnc4vk"
PASSWORD="password"

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
