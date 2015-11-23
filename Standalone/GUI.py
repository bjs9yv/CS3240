from tkinter import *
import threading
from Crypto.PublicKey import RSA
import KeyCheck
import os
import getpass
import requests
import re
from Crypto import Random

class SecureContactClient(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent, background="white")
		self.parent = parent
		self.parent.title("SecureContact Client")
		self.pack(fill=BOTH, expand=1)		
		self.initLoginFrame()
		self.centerWindow()

	def initLoginFrame(self):
		self.loginFrame = Frame(self, background="#c0c0c0")
		self.loginFrame.pack(fill=BOTH, expand=1)
		
		loginText = Message(self.loginFrame, text="Enter SecureContact Username: ")
		passText = Message(self.loginFrame, text="Enter SecureContact Password: ")
		loginText.config(bg='#f95252', bd=5, width=200, relief=RIDGE)
		passText.config(bg='#f95252', bd=5, width=200, relief=RIDGE)
		loginText.place(x=160, y=130)
		passText.place(x=160, y=170)

		self.loginFrame.loginEntry = Entry(self.loginFrame)
		self.loginFrame.passEntry = Entry(self.loginFrame, show="*")
		self.loginFrame.loginEntry.place(x=400, y=130)
		self.loginFrame.passEntry.place(x=400, y=170)

		loginButton = Button(self.loginFrame, text="Login", bg='#33cc77', command=self.grabDeets)
		loginButton.place(x=380, y=400)		

	def initMenu(self, frameId=None):
		temp = False
		if frameId is None:
			temp = self.loginFrame.first_time
			self.loginFrame.destroy()
		else:
			if frameId == 0:
				self.uploadFrame.destroy()
			elif frameId == 1:
				self.viewReportsFrame.destroy()
			else:
				pass
		self.menuFrame = Frame(self, background="#c0c0c0")
		self.menuFrame.pack(fill=BOTH, expand=1)

		if temp:
			firstTimeText = Message(self.menuFrame, text="Welcome to the SecureContactClient application!")
			firstTimeText.config(bg='#ffa500', bd=5, width=300, relief=RIDGE)
			firstTimeText.place(x=250, y=100)
			keyGeneratedText = Message(self.menuFrame, text="We've successfully generated a public/private RSA key pair for your account.")
			keyGeneratedText.config(bg='#ffa500', bd=5, width=600, relief=RIDGE)
			keyGeneratedText.place(x=100, y=180)

		viewReportsButton = Button(self.menuFrame, text="View Available Reports", bg='#33cc77', command=self.initViewReports)
		viewReportsButton.place(x=200, y=300)

		uploadButton = Button(self.menuFrame, text="Upload File", bg='#33cc77', command=self.initUpload)
		uploadButton.place(x=385, y=300)

		quitButton = Button(self.menuFrame, text="Quit", bg='#33cc77', command=self.quit)
		quitButton.place(x=500, y=300)

	def initViewReports(self):
		if self.menuFrame.winfo_exists() == 1:
			self.menuFrame.destroy()
		self.viewReportsFrame = Frame(self, background='#c0c0c0')
		self.viewReportsFrame.pack(fill=BOTH, expand=1)

		menuButton = Button(self.viewReportsFrame, text="Return to Menu", command= lambda :self.initMenu(1))
		menuButton.place(x=335, y=20)

		pullingReportsText = Message(self.viewReportsFrame, text="Pulling reports from secure server...")
		pullingReportsText.config(bg='#f95252', bd=5, width=250, relief=RIDGE)
		pullingReportsText.place(x=300, y=75)

		self.viewReportsFrame.reports = ["file.txt", "trapqueen.wapp", "wahoo.wa", "hortonhearsa.hoo"]
		y_list = []
		for i in range(0, len(self.viewReportsFrame.reports)):
			iText = Message(self.viewReportsFrame, text=i+1)
			reportText = Message(self.viewReportsFrame, text=self.viewReportsFrame.reports[i])
			reportButton = Button(self.viewReportsFrame, text="Download", command= lambda i=i: self.storeReportAt(i))
			iText.config(bg='#7ec0ee', bd=5, width=50, relief=RAISED)
			reportText.config(bg='#7ec0ee', bd=5, width=200, relief=RAISED)
			if i == 0:
				iText.place(x=260, y=150)
				reportText.place(x=300, y=150)
				reportButton.place(x=450, y=150)
				y_list.append(150)
			else:
				iText.place(x=260, y=y_list[i - 1] + 40)
				reportText.place(x=300, y=y_list[i - 1] + 40)
				reportButton.place(x=450, y=y_list[i - 1] + 40)
				y_list.append(y_list[i - 1] + 40)

	def initUpload(self):
		if self.menuFrame.winfo_exists() == 1:
			self.menuFrame.destroy()
		self.uploadFrame = Frame(self, background='#c0c0c0')
		self.uploadFrame.pack(fill=BOTH, expand=1)

		menuButton = Button(self.uploadFrame, text="Return to Menu", command= lambda: self.initMenu(0))
		menuButton.place(x=335, y=20)

		fileNameText = Message(self.uploadFrame, text="Enter the name of the file to upload")
		fileNameText.config(bg='#f95252', bd=5, width=280, relief=RIDGE)
		fileNameText.place(x=150, y=100)

		self.uploadFrame.fileNameEntry = Entry(self.uploadFrame)
		self.uploadFrame.fileNameEntry.place(x=400, y=100)

		uploadButton = Button(self.uploadFrame, text="Upload", command=self.uploadFile)
		uploadButton.place(x=580, y=100)

	def initEncryptUpload(self, buttonId=None):
		if not buttonId == None:
			fp = self.uploadFrame.file_paths_list[buttonId] + self.uploadFrame.file_name
		else:
			if self.uploadFrame.boolcheck and not self.uploadFrame.filePathEntry.get() == "":
				if not self.uploadFrame.filePathEntry.get()[len(self.uploadFrame.filePathEntry.get()) - 1] == '/':
					fp = self.uploadFrame.filePathEntry.get() + "/" + self.uploadFrame.file_name
				else:
					fp = self.uploadFrame.filePathEntry.get() + self.uploadFrame.file_name
			else:
				fp = self.uploadFrame.file_path
		self.uploadFrame.destroy()
		self.encryptUploadFrame = Frame(self, background='#c0c0c0')
		self.encryptUploadFrame.pack(fill=BOTH, expand=1)

		fileText = Message(self.encryptUploadFrame, text="File at: " + fp + " selected to upload.")
		fileText.config(bg='#f95252', bd=5, width=800, relief=RIDGE)
		fileText.place(x=50, y=100)

		encryptButton = Button(self.encryptUploadFrame, text="Encrypt & Upload", command=self.encryptUpload)
		encryptButton.place(x=250, y=140)
		noEncryptButton = Button(self.encryptUploadFrame, text="Upload Without Encryption", command=self.noEncryptUpload)
		noEncryptButton.place(x=400, y=140)

	def centerWindow(self):
		width = 800
		height = 500

		screen_width = self.parent.winfo_screenwidth()
		screen_height = self.parent.winfo_screenheight()

		x = (screen_width - width)/2
		y = (screen_height - height)/2

		self.parent.geometry("%dx%d+%d+%d" % (width, height, x, y))

	def grabDeets(self):
		passdic = {'username':self.loginFrame.loginEntry.get(),'password':self.loginFrame.passEntry.get()}
		response = requests.get('http://t16-heroku-app.herokuapp.com/check_login/', params=passdic)
		if response.json()['valid']:
			temp = False
			if not "PrivateKey.txt" in os.listdir(os.getcwd()): # TODO change this to search sub directory where keys are stored
				temp = True
				KeyCheck.gen_keys()
				# TODO: upload PublicKey.txt to db
			self.loginFrame.first_time = temp 
			self.initMenu()
		else:
			invalidDeetsText = Message(self, text="Invalid username and/or password, please try again.")
			invalidDeetsText.config(bg="white", bd=5, width=320, relief=GROOVE)
			invalidDeetsText.place(x=240, y=250)
			threading.Timer(3, invalidDeetsText.destroy, args=None).start()

	def uploadFile(self):
		self.uploadFrame.file_name = self.uploadFrame.fileNameEntry.get()
		self.uploadFrame.boolcheck = True
		root_check = False
		for item in os.listdir(os.getcwd()):
			if item == self.uploadFrame.file_name:
				self.uploadFrame.file_path = os.path.realpath(item)
				self.uploadFrame.boolcheck = False
				self.initEncryptUpload()
				root_check = True
				break
		if not root_check:
			notFoundText = Message(self.uploadFrame, text="The requested file is not within the current working directory.")
			notFoundText.config(bg="white", bd=5, width=400, relief=GROOVE)
			notFoundText.place(x=150, y=140)
			filePathText = Message(self.uploadFrame, text="Please specifiy the file path if known.")
			filePathText.place(x=150, y=180)
			filePathText.config(bg='#f95252', bd=5, width=300, relief=RIDGE)

			self.uploadFrame.filePathEntry = Entry(self.uploadFrame)
			self.uploadFrame.filePathEntry.place(x=400, y=180)
			filePathButton = Button(self.uploadFrame, text="Upload", command=self.initEncryptUpload)
			filePathButton.place(x=580, y=180)

			unknownButton = Button(self.uploadFrame, text="Path Unknown", command=self.findFile)
			unknownButton.place(x=580, y=216)

	def storeReportAt(self, buttonId):
		temp = self.viewReportsFrame.reports[buttonId]
		self.viewReportsFrame.destroy()

		self.downloadFrame = Frame(self, background='#c0c0c0')
		self.downloadFrame.pack(fill=BOTH, expand=1)
		self.downloadFrame.dl_file = temp

		dlFileText = Message(self.downloadFrame, text=self.downloadFrame.dl_file + " selected to download.")
		dlFileText.config(bg='#f95252', bd=5, width=300, relief=RIDGE)
		dlFileText.place(x=300, y=100)

		fileLocationText = Message(self.downloadFrame, text="Local file location:")
		fileLocationText.config(bg='#7ec0ee', bd=5, width=150, relief=RAISED)
		fileLocationText.place(x=150, y=180)

		self.downloadFrame.fileLocationEntry = Entry(self.downloadFrame)
		self.downloadFrame.fileLocationEntry.place(x=300, y=180)

		browseButton = Button(self.downloadFrame, text="Browse", command=self.browseFileSystem)
		browseButton.place(x=500, y=180)

		downloadButton = Button(self.downloadFrame, text="Download", command=self.downloadReport)
		downloadButton.place(x=590, y=180)

	def downloadReport(self):
		path = self.downloadFrame.fileLocationEntry.get()
		if len(path) == 0 or not path[len(path) - 1] == '/':
			path += '/'
		with open(path + self.downloadFrame.dl_file, 'w') as f:
			f.write("file_content") # Yea....
		self.downloadFrame.destroy()
		self.initViewReports()


	def findFile(self):
		file_path = ""
		check = False
		multiple = False
		file_paths = []
		for root, dirs, files in os.walk('/home'):
			for f in files:
				if f == self.uploadFrame.file_name:
					file_path = root + '/'
					file_paths.append(file_path)
					if not check:
						check = True
					else:
						multiple = True
		if multiple:
			multipleFilesText = Message(self.uploadFrame, text="Multiple files were found with the given filename.")
			multipleFilesText.config(bg='white', bd=5, width=320, relief=RIDGE)
			multipleFilesText.place(x=150, y=250)
			cntr = 1
			y_list = []
			self.uploadFrame.file_paths_list = []
			for f in file_paths:
				cntrText = Message(self.uploadFrame, text=str(cntr))
				cntrText.config(bg='#7ec0ee', bd=5, width=50, relief=RAISED)
				fileText = Message(self.uploadFrame, text=f + self.uploadFrame.file_name)
				fileText.config(bg='#7ec0ee', bd=5, width=560, relief=RAISED)
				fileButton = Button(self.uploadFrame, text="Upload", command= lambda cntr=cntr: self.initEncryptUpload(buttonId=cntr - 1))
				self.uploadFrame.file_paths_list.append(f)
				if cntr == 1:
					cntrText.place(x=150, y=290)
					fileText.place(x=180, y=290)
					fileButton.place(x=640, y=290)
					y_list.append(290)
				else:
					cntrText.place(x=150, y=y_list[cntr - 2] + 40)
					fileText.place(x=180, y=y_list[cntr - 2] + 40)
					fileButton.place(x=640, y=y_list[cntr - 2] + 40)
					y_list.append(y_list[cntr - 2] + 40)
				cntr += 1

	def encryptUpload(self):
		self.encryptUploadFrame.destroy()
		self.initUpload()
		pass

	def noEncryptUpload(self):
		self.encryptUploadFrame.destroy()
		self.initUpload()
		pass

	def browseFileSystem(self):
		self.downloadFrame.destroy()
		self.initViewReports()
		pass

def main():
	root = Tk()
	app = SecureContactClient(root)
	root.mainloop()

if __name__ == '__main__':
	main()