import sys
from sftptest import ClientSftp
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QPushButton, QListWidget)
 
class Screan(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.connection = None
        
    def initUI(self):
        self.hostEdit = QLineEdit(self)
        self.userEdit = QLineEdit()
        self.passwordEdit = QLineEdit()
        self.portEdit = QLineEdit()
        self.folders = QListWidget()
        self.curDirEdit = QLineEdit()
        btn1 = QPushButton("Connect", self)
        btn2 = QPushButton("Disconnect", self)
        grid = QGridLayout()

        #Данные сфтп, чтобы не запонлять
        self.hostEdit.setText('lenybot.ru')
        self.userEdit.setText('u0206471')
        self.passwordEdit.setText('8oE!v5cG')
        self.portEdit.setText('22') 

        btn1.clicked.connect(self.buttonConnect)
        btn2.clicked.connect(self.buttonDisconnect)
        grid.setSpacing(10)
        grid.addWidget(QLabel('Host'), 1, 0)
        grid.addWidget(self.hostEdit, 1, 1)
        grid.addWidget(QLabel('User'), 2, 0)
        grid.addWidget(self.userEdit, 2, 1)
        grid.addWidget(QLabel('Password'), 3, 0)
        grid.addWidget(self.passwordEdit, 3, 1)
        grid.addWidget(QLabel('Port'), 4, 0)
        grid.addWidget(self.portEdit, 4, 1)
        grid.addWidget(btn1, 5, 0)
        grid.addWidget(btn2, 5, 1)
        grid.addWidget(self.curDirEdit, 1, 2)
        grid.addWidget(self.folders, 2, 2, 4, 2)

        
        self.setLayout(grid) 
        
        #self.setGeometry(300, 300, 350, 300)
        self.show()

    def buttonConnect(self):
        try:
            self.connection = ClientSftp(self.hostEdit.text(), self.userEdit.text(), self.passwordEdit.text(), int(self.portEdit.text()))
            self.hostEdit.setReadOnly(True)
            self.userEdit.setReadOnly(True)
            self.passwordEdit.setReadOnly(True)
            self.portEdit.setReadOnly(True)
            self.folders.addItems(self.connection.folders)
            self.folders.itemDoubleClicked.connect(self.printDir)
            pass
        except Exception as e:
            print('cant connect')
            raise
    #Обновление окна текущей дирректории
    def refresfList(self):
        self.folders.clear()
        print(self.connection.folders)
        self.folders.addItems(self.connection.folders)
        #self.folders.itemDoubleClicked.connect(self.printDir)
        return True

    def buttonDisconnect(self):
        self.connection.close()
        self.hostEdit.setReadOnly(False)
        self.userEdit.setReadOnly(False)
        self.passwordEdit.setReadOnly(False)
        self.portEdit.setReadOnly(False)

    def printDir(self, item):
        if item.text() == '!!!UP':
            self.connection.fullAdr.pop(len(self.connection.fullAdr) - 1)
            self.curDirEdit.setText('/'.join(self.connection.fullAdr))
            self.connection.folders = self.connection.get_dir('/'.join(self.connection.fullAdr))
            self.refresfList()
        elif item.text()[0] == '/':
            self.connection.fullAdr.append(item.text()[1:])
            self.curDirEdit.setText('/'.join(self.connection.fullAdr))
            self.connection.folders = self.connection.get_dir('/'.join(self.connection.fullAdr))
            self.refresfList()
        else:
            print('it is a file')
            

        print(item.text())

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Screan()
    sys.exit(app.exec_())