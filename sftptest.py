import paramiko
import json

class ClientSftp:
	
	def __init__(self, hostname, username, password, port):
		self.host = hostname
		self.user = username
		self.password = password
		self.port = port		
		self.fullAdr = ['.'] #адрес текущей диррективы

		try:
			self.connect()

		except Exception as e:
			print('errr')
			raise	

	def connect(self):
		transport = paramiko.Transport((self.host, self.port))
		transport.connect(username = self.user, password = self.password)
		self.client = paramiko.SFTPClient.from_transport(transport)

	def close(self):
		self.client.close()

	def getDir(self):
		files = []
		directory = []

		if len(self.fullAdr) != 1 :
			directory.append('!!!UP')

		[directory.append('/' + dir) if self.isDir(dir) else files.append(dir) 
			for dir in self.client.listdir('/'.join(self.fullAdr))]

		directory.extend(files)
		return directory

	def isDir(self, dir):
		return 'd' in str(self.client.lstat('/'.join(self.fullAdr) + '/' + dir))

	def downloadFile(self, remote, local):
		self.client.get(remote, local)


class ClientLocal:
	
	def getConnectionList(self):
		connections_file = open('connections.json', 'r')
		return [key for key in json.load(connections_file)]

	def getConnectionInfo(self, connectionName):
		connections_file = open('connections.json', 'r')
		return json.load(connections_file)[connectionName]

	def saveConnectionInfo(self,connectionInfo):
		with open('connections.json', 'r') as file:
			connections = json.load(file)
			connections.update(connectionInfo)

		connections_file = open('connections.json', 'w')	
		connections_file.write(str(json.dumps(connections)))
		connections_file.close()