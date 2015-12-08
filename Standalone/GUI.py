from tkinter import *
import threading
from Crypto.PublicKey import RSA
import KeyCheck
import CheckAES
import os
import getpass
import requests
import re
from Crypto import Random
from tkinter import filedialog
from Crypto.Cipher import AES, PKCS1_OAEP
import base64

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
		self.usn = self.loginFrame.loginEntry.get()
		self.pwd = self.loginFrame.passEntry.get()
		passdic = {'username':self.usn,'password':self.pwd}
		response = requests.get('http://t16-heroku-app.herokuapp.com/check_login/', params=passdic)
		if response.json()['valid']:
			temp = False
			if not "AES_Key.txt" in os.listdir(os.getcwd()): # TODO change this to search sub directory where keys are stored
				temp = True
				#KeyCheck.gen_keys()
				CheckAES.gen_cipher()
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
			keyGeneratedText = Message(firstTimeFrame, text="We've successfully generated a public/private RSA key pair for your account, along with an AES cipher.")
			keyGeneratedText.config(bg='#ffa500', bd=5, width=300, relief=RIDGE)
			keyGeneratedText.grid(row=1, column=0)

		menuButtonsFrame = Frame(self.menuFrame, background='#c0c0c0')
		menuButtonsFrame.grid(row=1, column=0)
		viewReportsText = Message(menuButtonsFrame, text="1")
		viewReportsText.config(bg='#33cc77', bd=5, width=50, relief=RAISED)
		viewReportsText.grid(row=0, column=0)
		viewReportsButton = Button(menuButtonsFrame, text="View Available Reports", bg='#33cc77', command=self.initViewReports)
		viewReportsButton.grid(row=0, column=1)

		encryptFileText = Message(menuButtonsFrame, text="2")
		encryptFileText.config(bg='#33cc77', bd=5, width=50, relief=RAISED)
		encryptFileText.grid(row=1, column=0)
		encryptFileButton = Button(menuButtonsFrame, text="Encrypt Files", bg='#33cc77', command=self.initEncryptFiles)
		encryptFileButton.grid(row=1, column=1)

		uploadText = Message(menuButtonsFrame, text="3")
		uploadText.config(bg='#33cc77', bd=5, width=50, relief=RAISED)
		uploadText.grid(row=2, column=0)
		uploadButton = Button(menuButtonsFrame, text="Upload File", bg='#33cc77', command=self.initUpload)
		uploadButton.grid(row=2, column=1)

		quitText = Message(menuButtonsFrame, text="4")
		quitText.config(bg='#33cc77', bd=5, width=50, relief=RAISED)
		quitText.grid(row=3, column=0)
		quitButton = Button(menuButtonsFrame, text="Quit", bg='#33cc77', command=self.quit)
		quitButton.grid(row=3, column=1)

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

		passdic = {'username':self.usn,'password':self.pwd}
		response = requests.get('http://t16-heroku-app.herokuapp.com/get_reports/', params=passdic)
		if len(response.json()['reports']) == 0:
			noReportsTest = Message(self.viewReportsFrame, text="No reports found on the server.")
			noReportsTest.config(bg='#f95252', bd=5, width=200, relief=RIDGE)
			noReportsTest.grid(row=2, column=0)
		else:
			self.viewReportsFrame.reports = []
			for item in response.json()['reports']:
				self.viewReportsFrame.reports.append([item['description'], item['text'], item['files'], item['encrypted']])

			reportListFrame = Frame(self.viewReportsFrame, background='#c0c0c0')
			reportListFrame.grid(row=2, column=0)

			for i in range(0, len(self.viewReportsFrame.reports)):
				iText = Message(reportListFrame, text=i+1)
				reportText = Message(reportListFrame, text=self.viewReportsFrame.reports[i][0])
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

		dlFileText = Message(self.downloadFrame, text=self.downloadFrame.dl_file[0] + " selected to download.")
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

	def downloadReport(self, browsedDir=None):
		# Go to website endpoint and download actual file???
		path = ""
		if self.downloadFrame.winfo_exists() == 1:
			path = self.downloadFrame.fileLocationEntry.get()
		else:
			if not browsedDir == None:
				path = browsedDir
			else:
				self.downloadFrame.destroy()
				self.parent.geometry("")
				self.initViewReports()
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
			#try:
			f = open(path + self.downloadFrame.dl_file[0], 'w')
			f.write(self.downloadFrame.dl_file[1])
			for rf in self.downloadFrame.dl_file[2]:
				response = requests.get('http://t16-heroku-app.herokuapp.com' + rf, stream=True)
				split_url = rf.split('/')
				fln = split_url[len(split_url) - 1]
				try:
					new_file = open(path + fln, 'wb')
					if self.downloadFrame.dl_file[3]:
						dec_file = self.decryptFile(response.text)
						new_file.write(dec_file)
					else:
						for block in response.iter_content(1024):
							new_file.write(block)
				except Exception as e:
					print(e)
					continue
			self.downloadFrame.destroy()
			self.parent.geometry("")
			self.initViewReports()
			"""
			except:
				self.parent.geometry("")
				badPathText = Message(self.downloadFrame, text="Invalid path location, please try a different path.")
				badPathText.config(bg="#f95252", bd=5, width=400, relief=RIDGE)
				badPathText.grid(row=2, column=0)
				self.downloadFrame.update()
				self.centerWindow(w=self.downloadFrame.winfo_width(), h=self.downloadFrame.winfo_height())
				threading.Timer(3, badPathText.destroy, args=None).start()
				threading.Timer(3, self.centerWindow, (self.downloadFrame.winfo_width(), self.downloadFrame.winfo_height() - badPathText.winfo_height())).start()
			"""

	def decryptFile(self, b64d):
		ciphertext = base64.b64decode(b64d.encode())
		iv = ciphertext[:AES.block_size]
		bit_key = ""
		with open('./AES_Key.txt', 'rb') as f:
			bit_key = f.read()
		aes_guard = AES.new(bit_key, AES.MODE_CBC, iv)
		return self.unpad(aes_guard.decrypt(ciphertext[AES.block_size:]))

	def browseFileSystem(self):
		Tk.withdraw
		dn = filedialog.askdirectory()
		self.downloadFrame.destroy()
		self.parent.geometry("")
		self.downloadReport(browsedDir=dn)

	##############################################################################

	# -------------------------------------------------------------------------- #	
	# ------------------------------Encrypt Files------------------------------- #
	# -------------------------------------------------------------------------- #	

	def initEncryptFiles(self):
		if self.menuFrame.winfo_exists() == 1:
			self.menuFrame.destroy()
			self.parent.geometry("")
		self.encryptFileFrame = Frame(self, background='#c0c0c0')
		self.encryptFileFrame.pack(fill=BOTH, expand=1)

		self.encryptFileFrame.fileUIFrame = Frame(self.encryptFileFrame, background='#c0c0c0')
		self.encryptFileFrame.fileUIFrame.grid(row=0, column = 0)

		browseButton = Button(self.encryptFileFrame.fileUIFrame, text="Upload", command=self.browseFile)
		browseButton.grid(row=0, column=0)

		self.encryptFileFrame.update()
		self.centerWindow(w=self.encryptFileFrame.winfo_width(), h=self.encryptFileFrame.winfo_height())


	def browseFile(self):
		Tk.withdraw
		fn = filedialog.askopenfilename()
		self.encryptFileFrame.fn = fn
		self.parent.geometry("")

		fileNameText = Message(self.encryptFileFrame.fileUIFrame, text=fn)
		fileNameText.config(bg='#f95252', bd=5, width=280, relief=RIDGE)
		fileNameText.grid(row=0, column=1)

		encryptNoDelButton = Button(self.encryptFileFrame.fileUIFrame, text="Encrypt File", command=self.encFile)
		encryptNoDelButton.grid(row=1, column=0)

		encryptDelButton = Button(self.encryptFileFrame.fileUIFrame, text="Encrypt & Delete Original", command=self.encDelFile)
		encryptDelButton.grid(row=1, column=1)

		self.encryptFileFrame.update()
		self.centerWindow(w=self.encryptFileFrame.winfo_width(), h=self.encryptFileFrame.winfo_height())

	def encFile(self):
		file_contents = ""
		with open(self.encryptFileFrame.fn, 'rb') as f:
			file_contents = f.read()
		with open('./AES_Key.txt', 'rb') as f:
			enc_bit_key = f.read()
		r = Random.new()
		iv = r.read(AES.block_size)
		aes_guard = AES.new(enc_bit_key, AES.MODE_CBC, iv)
		ciphertext = aes_guard.encrypt(self.pad(file_contents))
		with open(self.encryptFileFrame.fn + ".enc", 'wb') as f:
			f.write(base64.b64encode(iv + ciphertext))
		self.encryptFileFrame.destroy()
		self.parent.geometry("")
		self.initMenu()

	def encDelFile(self):
		self.encryptFileFrame.destroy()
		self.parent.geometry("")
		self.initMenu()

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

			buttonFrame = Frame(self.uploadFrame, background='#c0c0c0')
			buttonFrame.grid(row=4, column=0)			

			filePathButton = Button(buttonFrame, text="Upload", command= lambda: self.initEncryptUpload(-2))
			filePathButton.grid(row=0, column=0)

			browseForFileButton = Button(buttonFrame, text="Browse", command=self.browseForFile)
			browseForFileButton.grid(row=0, column=1)

			unknownButton = Button(buttonFrame, text="Path Unknown", command= lambda: self.findFile(0))
			unknownButton.grid(row=0, column=2)

			self.uploadFrame.update()
			self.centerWindow(w=self.uploadFrame.winfo_width(), h=self.uploadFrame.winfo_height())
		else:
			if len(self.uploadFrame.local_file_paths) == 1:
				self.initEncryptUpload(-1)
			else:
				self.findFile(1)

	def findFile(self, mode):
		file_paths = []
		if mode == 0:
			file_path = ""
			for root, dirs, files in os.walk('/home'):
				for f in files:
					if f == self.uploadFrame.file_name:
						file_path = root + '/'
						file_paths.append(file_path)
		if len(file_paths) > 1 or mode == 1:
			self.parent.geometry("")

			multipleFilesText = Message(self.uploadFrame, text="Multiple files were found with the given filename.")
			multipleFilesText.config(bg='white', bd=5, width=320, relief=RIDGE)
			multipleFilesText.grid(row=5, column=0)

			multipleFilesFrame = Frame(self.uploadFrame, background='#c0c0c0')
			multipleFilesFrame.grid(row=6, column=0)
			cntr = 1
			if mode == 1:
				file_paths = self.uploadFrame.local_file_paths
			for f in file_paths:
				cntrText = Message(multipleFilesFrame, text=str(cntr))
				cntrText.config(bg='#7ec0ee', bd=5, width=50, relief=RAISED)
				fileText = Message(multipleFilesFrame, text=f + self.uploadFrame.file_name)
				fileText.config(bg='#7ec0ee', bd=5, width=560, relief=RAISED)
				fileButton = Button(multipleFilesFrame, text="Upload", command= lambda cntr=cntr: self.initEncryptUpload(cntr - 1))
				cntrText.grid(row=cntr - 1, column=0)
				fileText.grid(row=cntr - 1, column=1)
				fileButton.grid(row=cntr - 1, column=2)
				if mode == 0:
					self.uploadFrame.local_file_paths.append(f)
				cntr += 1
			self.uploadFrame.update()
			self.centerWindow(w=self.uploadFrame.winfo_width(), h=self.uploadFrame.winfo_height())
		elif len(file_paths) == 1:
			self.uploadFrame.local_file_paths.append(file_path + self.uploadFrame.file_name)
			self.initEncryptUpload(-1)
		else:
			self.parent.geometry("")

			noFileText = Message(self.uploadFrame, text="No such files were found on the local system.")
			noFileText.config(bg='white', bd=5, width=320, relief=RIDGE)
			noFileText.grid(row=5, column=0)
			
			self.uploadFrame.update()
			self.centerWindow(w=self.uploadFrame.winfo_width(), h=self.uploadFrame.winfo_height())
		
	def initEncryptUpload(self, mode):
		fp = ""
		if mode == -1:
			fp = self.uploadFrame.local_file_paths[0]
		elif mode == -2:
			fp = self.uploadFrame.filePathEntry.get()
			if not fp[len(fp) - 1] == '/':
				fp += '/'
				fp += self.uploadFrame.file_name
			else:
				fp += self.uploadFrame.file_name
		else:
			fp = self.uploadFrame.local_file_paths[mode] + self.uploadFrame.file_name

		if self.uploadFrame.winfo_exists() == 1:
			self.uploadFrame.destroy()
			self.parent.geometry("")

		self.encryptUploadFrame = Frame(self, background='#c0c0c0')
		self.encryptUploadFrame.pack(fill=BOTH, expand=1)

		fileText = Message(self.encryptUploadFrame, text="File at: " + str(fp) + " selected to upload.")
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

	def browseForFile(self):
		Tk.withdraw
		fn = filedialog.askopenfilename()
		self.uploadFrame.local_file_paths.append(fn)
		self.initEncryptUpload(-1)

	def encryptUpload(self):
		self.encryptUploadFrame.destroy()
		self.parent.geometry("")
		self.initUpload()

	def noEncryptUpload(self):
		self.encryptUploadFrame.destroy()
		self.parent.geometry("")
		self.initUpload()

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

	def pad(self, message):
		togo = AES.block_size - (len(message) % AES.block_size)
		return message + (chr(togo)*togo).encode()

	def unpad(self, padded):
		num = padded[-1]
		return padded[:-num]

def main():
	root = Tk()
	app = SecureContactClient(root)
	root.mainloop()

if __name__ == '__main__':
	main()