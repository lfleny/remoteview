import paramiko

host = "lenybot.ru"
user = "u0206471"
password = "8oE!v5cG"
port = 22

class ClientSftp:
	
	def __init__(self, hostname, username, password, port):
		self.client = None
#		self.host = "lenybot.ru"
#		self.user = "u0206471"
#		self.password = "8oE!v5cG"
#		self.port = 22

		self.host = hostname
		self.user = username
		self.password = password
		self.port = port

		self.cd = ''
		self.folders = []

		try:
			self.connect()
			self.folders = self.get_dir('')

		except Exception as e:
			print('errr')
			raise
		

	def connect(self):
		transport = paramiko.Transport((self.host, self.port))
		transport.connect(username = self.user, password = self.password)
		self.client = paramiko.SFTPClient.from_transport(transport)

	def run(self):
		self.connect()
		while 1:
			print('enter command: \n')
			ddr = input()
			if (ddr == 'break'):
				self.close()
				break
			elif ('cd' in ddr):
				if (ddr == 'cd'):
					print(self.cd)
				elif (len(ddr) > 3):
					self.cd = ddr[3:]
					print(self.cd)
				else:
					print('errr')
			else:
				try:
					self.get_dir(str(ddr))
					pass
				except Exception as e:
					print('Wrong dir')
					pass

	def close(self):
		self.client.close()

	def get_dir(self, adress):
		if (adress.strip() == ''):
			adr = '.'
		else:
			adr = './' + adress.strip()

		dirlist = self.client.listdir(adr)
		files = []
		directory = []
		for dir in dirlist:
			if 'd' in str(self.client.lstat('./' + adress + '/' + dir)): 
				directory.append(dir)
			else:
				files.append(dir)

		for d in directory:
			d = '/' + d

#		for f in files:
#			print('' + f)

		return directory




#print('Current directory:')
#open_dir('')

#result = ClientSftp('','','',123)
#result.run()





#dirlist = client.listdir('.')
#files = []
#directory = []
#for dir in dirlist:
#	if 'd' in str(client.lstat('' + dir)): 
#		directory.append(dir)
#	else:
#		files.append(dir)



#for d in directory:
#	open_dir(d)

#for f in files:
#	print(f)


#print(client.listdir('./www'))
#client.close()

