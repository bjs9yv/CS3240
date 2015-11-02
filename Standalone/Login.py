__author__ = 'adminuser'

USERNAME="bnc4vk"
PASSWORD="password"

print("Launching standalone application...\n")

check = True
while check:
    usr = input("Enter username: ")
    if usr == USERNAME:
        check = False
        while True:
            pswd = input("Enter password: ")
            if pswd == PASSWORD:
                break
    else:
        print("Username not recognized, please try again")

print("Available reports:")

reports = 5

for i in range(5):
    print("Report [" + str(i) + "]:")

command_list = ['DOWNLOAD', '...', '..', '.']

for item in command_list:
    print(item)

command = input("Choose command")

if command == "DOWNLOAD":
    file = input("Choose file to download")
