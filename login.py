from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from os import path
import sys
from main import MainApp
from signup import SignApp
import pymysql
import qdarkstyle


FORM_CLASS,s= loadUiType(path.join(path.dirname(__file__),'login.ui'))
class LoginApp(QDialog,FORM_CLASS):
    def __init__(self,parent=None):
        super(LoginApp, self).__init__(parent)
        QDialog.__init__(self)
        self.setupUi(self)
        self.Handle_Ui()
        self.Handle_Buttons()
        # self.Handle_table()
    def Handle_Ui(self):
        self.setWindowTitle('Login OMR System')
        self.setWindowIcon(QIcon('send-user.png'))
        # label1 = self.label
        # pixmap1 = QPixmap('send-user.png')
        #
        # label1.setPixmap(pixmap1)
        # label1.setScaledContents(True)
        # label1.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)

    def Handle_Buttons(self):
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.open_signup)
    def open_signup(self):
        self.sign_obj=SignApp()
        self.hide()
        self.sign_obj.show()
    def open_main(self):
        pass

    def login(self):
        user=self.lineEdit.text()
        password=self.lineEdit_2.text()
        db = pymysql.connect("localhost", 'root', '', 'omr')
        sql1 = """ SELECT * FROM doctors WHERE email= '{}'and password='{}'  """.format(user,password)
        cursor = db.cursor()
        cursor.execute(sql1)
        res = cursor.fetchall()

        if len(res)>0:
            self.main_obj = MainApp()
            self.hide()
            self.main_obj.show()
            self.main_obj.label_4.setText('{}'.format(user))
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("authentication error")
            msg.setInformativeText("username and email do not match ")
            msg.setWindowTitle("authentication error")
            msg.exec_()
        db.close()


def main():
    app=QApplication(sys.argv)
    window=LoginApp()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window.show()
    app.exec_()
main()