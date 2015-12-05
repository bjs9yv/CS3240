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

	# -------------------------------------------------------------------------- #	
	# ------------------------------Login Protocol------------------------------ #
	# -------------------------------------------------------------------------- #

	def initLoginFrame(self):
		self.loginFrame = Frame(self, background="#c0c0c0")
		self.loginFrame.pack(fill=BOTH, expand=1)
		
		secureIcon = PhotoImage(file="./GUI_Content/SecureContact.png")
		imageLabel = Label(self.loginFrame, image=secureIcon)
		imageLabel.photo = secureIcon
		imageLabel.grid(row=0, column=0)

		detailsFrame = Frame(self.loginFrame, background='#c0c0c0')
		detailsFrame.grid(row=2, column=0)

		loginText = Message(detailsFrame, text="Enter SecureContact Username: ")
		passText = Message(detailsFrame, text="Enter SecureContact Password: ")
		loginText.config(bg='#f95252', bd=5, width=200, relief=RIDGE)
		loginText.grid(row=0, column=0)
		passText.config(bg='#f95252', bd=5, width=200, relief=RIDGE)
		passText.grid(row=1, column=0)

		self.loginFrame.loginEntry = Entry(detailsFrame)
		self.loginFrame.loginEntry.grid(row=0, column=1)
		self.loginFrame.passEntry = Entry(detailsFrame, show="*")
		self.loginFrame.passEntry.grid(row=1, column=1)

		loginButton = Button(self.loginFrame, text="Login", bg='#33cc77', command=self.grabDeets)
		loginButton.grid(row=3, column=0)

		self.loginFrame.update()
		self.centerWindow(w=self.loginFrame.winfo_width(), h=self.loginFrame.winfo_height())

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
			invalidDeetsText = Message(self.loginFrame, text="Invalid username and/or password, please try again.")
			invalidDeetsText.config(bg="white", bd=5, width=320, relief=GROOVE)
			invalidDeetsText.grid(row=1, column=0)
			invalidDeetsText.update()
			self.centerWindow(w=self.loginFrame.winfo_width(), h=self.loginFrame.winfo_height() + invalidDeetsText.winfo_height())
			threading.Timer(3, invalidDeetsText.destroy, args=None).start()
			threading.Timer(3, self.centerWindow, [self.loginFrame.winfo_width(), self.loginFrame.winfo_height()]).start()

	##############################################################################

	# -------------------------------------------------------------------------- #	
	# --------------------------------Main Menu--------------------------------- #
	# -------------------------------------------------------------------------- #

	def initMenu(self, frameId=None):
		temp = False
		if frameId is None:
			if self.loginFrame.winfo_exists() == 1:
				temp = self.loginFrame.first_time
				self.loginFrame.destroy()
				self.parent.geometry("")
		else:
			if frameId == 0:
				if self.uploadFrame.winfo_exists() == 1:
					self.uploadFrame.destroy()
					self.parent.geometry("")
			elif frameId == 1:
				if self.viewReportsFrame.winfo_exists() == 1:
					self.viewReportsFrame.destroy()
					self.parent.geometry("")
			else:
				pass
		self.menuFrame = Frame(self, background="#c0c0c0")
		self.menuFrame.pack(fill=BOTH, expand=1)

		if temp:
			firstTimeFrame = Frame(self.menuFrame, background='#c0c0c0')
			firstTimeFrame.grid(row=0, column=0)
			firstTimeText = Message(firstTimeFrame, text="Welcome to the SecureContactClient application!")
			firstTimeText.config(bg='#ffa500', bd=5, width=300, relief=RIDGE)
			firstTimeText.grid(row=0, column=0)
			keyGeneratedText = Message(firstTimeFrame, text="We've successfully generated a public/private RSA key pair for your account.")
			keyGeneratedText.config(bg='#ffa500', bd=5, width=600, relief=RIDGE)
			keyGeneratedText.grid(row=1, column=0)

		menuButtonsFrame = Frame(self.menuFrame, background='#c0c0c0')
		menuButtonsFrame.grid(row=1, column=0)
		viewReportsText = Message(menuButtonsFrame, text="1")
		viewReportsText.config(bg='#33cc77', bd=5, width=50, relief=RAISED)
		viewReportsText.grid(row=0, column=0)
		viewReportsButton = Button(menuButtonsFrame, text="View Available Reports", bg='#33cc77', command=self.initViewReports)
		viewReportsButton.grid(row=0, column=1)

		uploadText = Message(menuButtonsFrame, text="2")
		uploadText.config(bg='#33cc77', bd=5, width=50, relief=RAISED)
		uploadText.grid(row=1, column=0)
		uploadButton = Button(menuButtonsFrame, text="Upload File", bg='#33cc77', command=self.initUpload)
		uploadButton.grid(row=1, column=1)

		quitText = Message(menuButtonsFrame, text="3")
		quitText.config(bg='#33cc77', bd=5, width=50, relief=RAISED)
		quitText.grid(row=2, column=0)
		quitButton = Button(menuButtonsFrame, text="Quit", bg='#33cc77', command=self.quit)
		quitButton.grid(row=2, column=1)

		self.menuFrame.update()
		self.centerWindow(w=self.menuFrame.winfo_width(), h=self.menuFrame.winfo_height())

	##############################################################################

	# -------------------------------------------------------------------------- #	
	# -------------------------------View Reports------------------------------- #
	# -------------------------------------------------------------------------- #

	def initViewReports(self):
		if self.menuFrame.winfo_exists() == 1:
			self.menuFrame.destroy()
			self.parent.geometry("")
		self.viewReportsFrame = Frame(self, background='#c0c0c0')
		self.viewReportsFrame.pack(fill=BOTH, expand=1)

		menuButton = Button(self.viewReportsFrame, text="Return to Menu", command= lambda :self.initMenu(1))
		menuButton.grid(row=0, column=0)

		pullingReportsText = Message(self.viewReportsFrame, text="Pulling reports from secure server...")
		pullingReportsText.config(bg='#f95252', bd=5, width=250, relief=RIDGE)
		pullingReportsText.grid(row=1, column=0)

		self.viewReportsFrame.reports = ["file.txt", "trapqueen.wapp", "wahoo.wa", "hortonhearsa.hoo"]
		reportListFrame = Frame(self.viewReportsFrame, background='#c0c0c0')
		reportListFrame.grid(row=2, column=0)
		for i in range(0, len(self.viewReportsFrame.reports)):
			iText = Message(reportListFrame, text=i+1)
			reportText = Message(reportListFrame, text=self.viewReportsFrame.reports[i])
			reportButton = Button(reportListFrame, text="Download", command= lambda i=i: self.storeReportAt(i))
			iText.config(bg='#7ec0ee', bd=5, width=50, relief=RAISED)
			reportText.config(bg='#7ec0ee', bd=5, width=200, relief=RAISED)
			iText.grid(row=i, column=0)
			reportText.grid(row=i, column=1)
			reportButton.grid(row=i, column=2)

		self.viewReportsFrame.update()
		self.centerWindow(w=self.viewReportsFrame.winfo_width(), h=self.viewReportsFrame.winfo_height())
	
	def storeReportAt(self, buttonId):
		temp = self.viewReportsFrame.reports[buttonId]
		self.viewReportsFrame.destroy()
		self.parent.geometry("")

		self.downloadFrame = Frame(self, background='#c0c0c0')
		self.downloadFrame.pack(fill=BOTH, expand=1)
		self.downloadFrame.dl_file = temp

		dlFileText = Message(self.downloadFrame, text=self.downloadFrame.dl_file + " selected to download.")
		dlFileText.config(bg='#f95252', bd=5, width=300, relief=RIDGE)
		dlFileText.grid(row=0, column=0)

		pathFrame = Frame(self.downloadFrame, background='#c0c0c0')
		pathFrame.grid(row=1, column=0)

		fileLocationText = Message(pathFrame, text="Local file location:")
		fileLocationText.config(bg='#7ec0ee', bd=5, width=150, relief=RAISED)
		fileLocationText.grid(row=0, column=0)

		self.downloadFrame.fileLocationEntry = Entry(pathFrame)
		self.downloadFrame.fileLocationEntry.grid(row=0, column=1)

		browseButton = Button(pathFrame, text="Browse", command=self.browseFileSystem)
		browseButton.grid(row=0, column=2)

		downloadButton = Button(pathFrame, text="Download", command=self.downloadReport)
		downloadButton.grid(row=0, column=3)

		self.downloadFrame.update()
		self.centerWindow(w=self.downloadFrame.winfo_width(), h=self.downloadFrame.winfo_height())

	def downloadReport(self):
		path = self.downloadFrame.fileLocationEntry.get()
		if len(path) == 0:
			self.parent.geometry("")
			noPathText = Message(self.downloadFrame, text="Please enter a path location to store the file at.")
			noPathText.config(bg="#f95252", bd=5, width=400, relief=RIDGE)
			noPathText.grid(row=2, column=0)
			self.downloadFrame.update()
			self.centerWindow(w=self.downloadFrame.winfo_width(), h=self.downloadFrame.winfo_height())
			threading.Timer(3, noPathText.destroy, args=None).start()
			threading.Timer(3, self.centerWindow, (self.downloadFrame.winfo_width(), self.downloadFrame.winfo_height() - noPathText.winfo_height())).start()
		else:
			if not path[len(path) - 1] == '/':
				path += '/'
			try:
				f = open(path + self.downloadFrame.dl_file, 'w')
				f.write("file_content") # Yea....
				self.downloadFrame.destroy()
				self.parent.geometry("")
				self.initViewReports()
			except:
				self.parent.geometry("")
				badPathText = Message(self.downloadFrame, text="Invalid path location, please try a different path.")
				badPathText.config(bg="#f95252", bd=5, width=400, relief=RIDGE)
				badPathText.grid(row=2, column=0)
				self.downloadFrame.update()
				self.centerWindow(w=self.downloadFrame.winfo_width(), h=self.downloadFrame.winfo_height())
				threading.Timer(3, badPathText.destroy, args=None).start()
				threading.Timer(3, self.centerWindow, (self.downloadFrame.winfo_width(), self.downloadFrame.winfo_height() - badPathText.winfo_height())).start()

	def browseFileSystem(self):
		self.downloadFrame.destroy()
		self.parent.geometry("")
		self.initViewReports()
		pass

	##############################################################################


	# -------------------------------------------------------------------------- #	
	# ------------------------------Upload Report------------------------------- #
	# -------------------------------------------------------------------------- #

	def initUpload(self):
		if self.menuFrame.winfo_exists() == 1:
			self.menuFrame.destroy()
			self.parent.geometry("")
		self.uploadFrame = Frame(self, background='#c0c0c0')
		self.uploadFrame.pack(fill=BOTH, expand=1)

		menuButton = Button(self.uploadFrame, text="Return to Menu", command= lambda: self.initMenu(0))
		menuButton.grid(row=0, column=0)

		fileNameFrame = Frame(self.uploadFrame, background='#c0c0c0')
		fileNameFrame.grid(row=1, column=0)

		fileNameText = Message(fileNameFrame, text="Enter the name of the file to upload")
		fileNameText.config(bg='#f95252', bd=5, width=280, relief=RIDGE)
		fileNameText.grid(row=0, column=0)

		self.uploadFrame.fileNameEntry = Entry(fileNameFrame)
		self.uploadFrame.fileNameEntry.grid(row=0, column=1)

		uploadButton = Button(fileNameFrame, text="Upload", command=self.uploadFile)
		uploadButton.grid(row=0, column=2)

		self.uploadFrame.update()
		self.centerWindow(w=self.uploadFrame.winfo_width(), h=self.uploadFrame.winfo_height())

	def uploadFile(self):
		self.uploadFrame.file_name = self.uploadFrame.fileNameEntry.get()
		self.uploadFrame.local_file_paths = []
		self.uploadFrame.boolcheck = True
		root_check = False
		for root, dirs, files in os.walk(os.getcwd()):
				for f in files:
					if f == self.uploadFrame.file_name:
						self.uploadFrame.local_file_paths.append(root + '/')
						self.uploadFrame.boolcheck = False
						root_check = True
		if not root_check:
			self.parent.geometry("")

			notFoundText = Message(self.uploadFrame, text="The requested file is not within the current working directory.")
			notFoundText.config(bg="white", bd=5, width=400, relief=GROOVE)
			notFoundText.grid(row=2, column=0)

			fileNotFoundFrame = Frame(self.uploadFrame, background='#c0c0c0')
			fileNotFoundFrame.grid(row=3, column=0)

			filePathText = Message(fileNotFoundFrame, text="Please specifiy the file path if known.")
			filePathText.config(bg='#f95252', bd=5, width=300, relief=RIDGE)
			filePathText.grid(row=0, column=0)

			self.uploadFrame.filePathEntry = Entry(fileNotFoundFrame)
			self.uploadFrame.filePathEntry.grid(row=0, column=1)

			filePathButton = Button(fileNotFoundFrame, text="Upload", command=self.initEncryptUpload)
			filePathButton.grid(row=0, column=2)

			unknownButton = Button(fileNotFoundFrame, text="Path Unknown", command=self.findFile)
			unknownButton.grid(row=1, column=2)

			self.uploadFrame.update()
			self.centerWindow(w=self.uploadFrame.winfo_width(), h=self.uploadFrame.winfo_height())
		else:

			if len(self.uploadFrame.local_file_paths) == 1:
				self.initEncryptUpload()
			else:
				self.findFile(mode=1)

	def findFile(self, mode=None):
		if mode == None:
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
				self.parent.geometry("")

				multipleFilesText = Message(self.uploadFrame, text="Multiple files were found with the given filename.")
				multipleFilesText.config(bg='white', bd=5, width=320, relief=RIDGE)
				multipleFilesText.grid(row=4, column=0)

				multipleFilesFrame = Frame(self.uploadFrame, background='#c0c0c0')
				multipleFilesFrame.grid(row=5, column=0)
				cntr = 1
				self.uploadFrame.file_paths_list = []
				for f in file_paths:
					cntrText = Message(multipleFilesFrame, text=str(cntr))
					cntrText.config(bg='#7ec0ee', bd=5, width=50, relief=RAISED)
					fileText = Message(multipleFilesFrame, text=f + self.uploadFrame.file_name)
					fileText.config(bg='#7ec0ee', bd=5, width=560, relief=RAISED)
					fileButton = Button(multipleFilesFrame, text="Upload", command= lambda cntr=cntr: self.initEncryptUpload(buttonId=cntr - 1))
					cntrText.grid(row=cntr - 1, column=0)
					fileText.grid(row=cntr - 1, column=1)
					fileButton.grid(row=cntr - 1, column=2)
					self.uploadFrame.file_paths_list.append(f)
					cntr += 1

				self.uploadFrame.update()
				self.centerWindow(w=self.uploadFrame.winfo_width(), h=self.uploadFrame.winfo_height())
			else:
				self.uploadFrame.file_paths_list = []
				self.uploadFrame.file_paths_list.append(file_path)
				self.initEncryptUpload()
		else:
			self.parent.geometry("")

			multipleFilesText = Message(self.uploadFrame, text="Multiple files were found with the given filename.")
			multipleFilesText.config(bg='white', bd=5, width=320, relief=RIDGE)
			multipleFilesText.grid(row=4, column=0)

			multipleFilesFrame = Frame(self.uploadFrame, background='#c0c0c0')
			multipleFilesFrame.grid(row=5, column=0)
			cntr = 1
			self.uploadFrame.file_paths_list = []
			for f in self.uploadFrame.local_file_paths:
				cntrText = Message(multipleFilesFrame, text=str(cntr))
				cntrText.config(bg='#7ec0ee', bd=5, width=50, relief=RAISED)
				fileText = Message(multipleFilesFrame, text=f + self.uploadFrame.file_name)
				fileText.config(bg='#7ec0ee', bd=5, width=560, relief=RAISED)
				fileButton = Button(multipleFilesFrame, text="Upload", command= lambda cntr=cntr: self.initEncryptUpload(buttonId=cntr - 1))
				cntrText.grid(row=cntr - 1, column=0)
				fileText.grid(row=cntr - 1, column=1)
				fileButton.grid(row=cntr - 1, column=2)
				self.uploadFrame.file_paths_list.append(f)
				cntr += 1

			self.uploadFrame.update()
			self.centerWindow(w=self.uploadFrame.winfo_width(), h=self.uploadFrame.winfo_height())

	def initEncryptUpload(self, buttonId=None):
		if not buttonId == None:
			fp = self.uploadFrame.file_paths_list[buttonId] + self.uploadFrame.file_name
		else:
			if self.uploadFrame.boolcheck and not self.uploadFrame.filePathEntry.get() == "":
				if not self.uploadFrame.filePathEntry.get()[len(self.uploadFrame.filePathEntry.get()) - 1] == '/':
					fp = self.uploadFrame.filePathEntry.get() + "/" + self.uploadFrame.file_name
				else:
					fp = self.uploadFrame.filePathEntry.get() + self.uploadFrame.file_name
			elif self.uploadFrame.boolcheck:
				fp = self.uploadFrame.file_paths_list[0] + self.uploadFrame.file_name
			else:
				fp = self.uploadFrame.local_file_paths[0]

		if self.uploadFrame.winfo_exists() == 1:
			self.uploadFrame.destroy()
			self.parent.geometry("")

		self.encryptUploadFrame = Frame(self, background='#c0c0c0')
		self.encryptUploadFrame.pack(fill=BOTH, expand=1)

		fileText = Message(self.encryptUploadFrame, text="File at: " + fp + " selected to upload.")
		fileText.config(bg='#f95252', bd=5, width=800, relief=RIDGE)
		fileText.grid(row=0, column=0)

		encryptionFrame = Frame(self.encryptUploadFrame, background='#c0c0c0')
		encryptionFrame.grid(row=1, column=0)

		encryptButton = Button(encryptionFrame, text="Encrypt & Upload", command=self.encryptUpload)
		encryptButton.grid(row=0, column=0)
		noEncryptButton = Button(encryptionFrame, text="Upload Without Encryption", command=self.noEncryptUpload)
		noEncryptButton.grid(row=0, column=1)

		self.encryptUploadFrame.update()
		self.centerWindow(w=self.encryptUploadFrame.winfo_width(), h=self.encryptUploadFrame.winfo_height())

	def encryptUpload(self):
		self.encryptUploadFrame.destroy()
		self.parent.geometry("")
		self.initUpload()
		pass

	def noEncryptUpload(self):
		self.encryptUploadFrame.destroy()
		self.parent.geometry("")
		self.initUpload()
		pass

	##############################################################################

	# -------------------------------------------------------------------------- #	
	# --------------------------------Utilities--------------------------------- #
	# -------------------------------------------------------------------------- #

	def centerWindow(self, w=650, h=195):
		width = w
		height = h

		screen_width = self.parent.winfo_screenwidth()
		screen_height = self.parent.winfo_screenheight()

		x = (screen_width - width)/2
		y = (screen_height - height)/2

		self.parent.geometry("%dx%d+%d+%d" % (width, height, x, y))

def main():
	root = Tk()
	app = SecureContactClient(root)
	root.mainloop()

if __name__ == '__main__':
	main()