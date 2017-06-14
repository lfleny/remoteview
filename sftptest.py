import paramiko

class ClientSftp:
	
	def __init__(self, hostname, username, password, port):
		self.client = None
		self.host = hostname
		self.user = username
		self.password = password
		self.port = port

		
		self.folders = []

		#адрес текущей диррективы
		self.fullAdr = ['.']

		try:
			self.connect()
			self.folders = self.get_dir()

		except Exception as e:
			print('errr')
			raise
		

	def connect(self):
		transport = paramiko.Transport((self.host, self.port))
		transport.connect(username = self.user, password = self.password)
		self.client = paramiko.SFTPClient.from_transport(transport)

	def close(self):
		self.client.close()

	def get_dir(self, adress = '.'):

		files = []
		directory = []

		if adress != '.':
			directory.append('!!!UP')

		dirlist = self.client.listdir(adress.strip())

		for dir in dirlist:
			if 'd' in str(self.client.lstat(adress + '/' + dir)):
				directory.append('/' + dir)
			else:
				files.append(dir)

		res = directory.copy()
		res.extend(files)

		return res

	def downloadFile(self, remote, local):
		self.client.get(local,remote)
		return True