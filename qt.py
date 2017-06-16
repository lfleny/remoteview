import sys
from sftptest import (ClientSftp, ClientLocal)
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QComboBox,
                            QApplication, QPushButton, QListWidget)

import logging

logging.basicConfig(filename='example.log', level=logging.DEBUG)
 
class Screan(QWidget):
    
    def __init__(self):
        super().__init__()
        self.localClient = ClientLocal()
        self.initUI()
        
    def initUI(self):
        self.folders = QListWidget()
        self.curDirEdit = QLineEdit()
        self.btnConnect = QPushButton("Connect", self)
        self.btnDisconnect = QPushButton("Disconnect", self)
        grid = QGridLayout()

        self.connectionList = QComboBox(self)
        self.connectionList.addItem('Новое подключение')
        self.connectionList.addItems(self.localClient.getConnectionList())
        self.connectionList.activated[str].connect(self.setConnectionData)

        self.btnConnect.clicked.connect(self.buttonConnect)
        self.btnDisconnect.clicked.connect(self.buttonDisconnect)

        self.btnConnect.setEnabled(False)
        self.btnDisconnect.setEnabled(False)
        grid.setSpacing(10)
        grid.addWidget(self.connectionList, 1, 0)
        grid.addWidget(self.btnConnect, 1, 1)
        grid.addWidget(self.btnDisconnect, 1, 2)
        grid.addWidget(self.curDirEdit, 2, 0, 2, 2)
        grid.addWidget(self.folders, 4, 0, 5, 2)
        
        self.setLayout(grid) 
        self.show()

    def buttonConnect(self):
        try:
            self.connection = ClientSftp(self.connectionData['host'], self.connectionData['user'], 
                                self.connectionData['password'], int(self.connectionData['port']))
            self.folders.addItems(self.connection.getDir())
            self.folders.itemDoubleClicked.connect(self.printDir)
            self.btnDisconnect.setEnabled(True)
            self.btnConnect.setEnabled(False)
            self.connectionList.setEnabled(False)
            pass
        except Exception as e:
            print('cant connect')
            raise
    #Обновление окна текущей дирректории
    def refresfList(self):
        self.folders.clear()
        self.folders.addItems(self.connection.folders)

    def buttonDisconnect(self):
        self.connection.close()
        self.folders.clear()
        self.btnConnect.setEnabled(True)
        self.btnDisconnect.setEnabled(False)
        self.connectionList.setEnabled(True)

    def printDir(self, item):
        try:
            if item.text() == '!!!UP':
                self.connection.fullAdr.pop(len(self.connection.fullAdr) - 1)
                self.curDirEdit.setText('/'.join(self.connection.fullAdr))
                self.connection.folders = self.connection.getDir()
                self.refresfList()
            elif item.text()[0] == '/':
                self.connection.fullAdr.append(item.text()[1:])
                self.curDirEdit.setText('/'.join(self.connection.fullAdr))
                self.connection.folders = self.connection.getDir()
                self.refresfList()
            elif item.text()[0] != '/':
                path = '/'.join(self.connection.fullAdr) + '/' + item.text()
                self.connection.downloadFile(path, item.text())
                print('it is a file')
        except BaseException:
            logging.getLogger(__name__).exception("Program terminated")
            raise

    def openExplorer():

        return True

    def setConnectionData(self, text):
        if text in self.localClient.getConnectionList():
            self.connectionData = self.localClient.getConnectionInfo(text)
            self.btnConnect.setEnabled(True)
        else:
            self.btnConnect.setEnabled(False)
            self.createNewConnection()
            print("nothing")
        
    def createNewConnection(self):
        self.newConnectionPopup = newConnectionPopup("New connection")
        self.newConnectionPopup.show()

class newConnectionPopup(QWidget):
    def __init__(self, name):
        super().__init__()

        self.name = name
        self.initUI()
        self.setGeometry(300, 300, 350, 300)

    def initUI(self):
        self.hostEdit = QLineEdit(self)
        self.userEdit = QLineEdit()
        self.passwordEdit = QLineEdit()
        self.portEdit = QLineEdit()
        self.folders = QListWidget()
        self.curDirEdit = QLineEdit()
        btnSaveConnecction = QPushButton("Save", self)
        btnSaveConnecction.clicked.connect(self.buttSave)
        grid = QGridLayout()
        
        grid.setSpacing(10)
        grid.addWidget(QLabel('Host'), 1, 0)
        grid.addWidget(self.hostEdit, 1, 1)
        grid.addWidget(QLabel('User'), 2, 0)
        grid.addWidget(self.userEdit, 2, 1)
        grid.addWidget(QLabel('Password'), 3, 0)
        grid.addWidget(self.passwordEdit, 3, 1)
        grid.addWidget(QLabel('Port'), 4, 0)
        grid.addWidget(self.portEdit, 4, 1)
        grid.addWidget(btnSaveConnecction, 5, 1, 5, 2)

        # adjust the margins or you will get an invisible, unintended border
        grid.setContentsMargins(10, 10, 10, 10)
        # need to set the layout
        self.setLayout(grid)

    def buttSave(self):
        self.localClient = ClientLocal()
        info = {
        "host" : "test.ru",
        "user" : "test",
        "password" : "123",
        "port" : 22
        }
        dict = {"new" : info}
        self.localClient.saveConnectionInfo(dict)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Screan()
    sys.exit(app.exec_())
