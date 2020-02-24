from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import qdarkstyle
from os import path
import sys
import pymysql
from main import MainApp

FORM_CLASS,s= loadUiType(path.join(path.dirname(__file__),'signup.ui'))
class SignApp(QDialog,FORM_CLASS):
    def __init__(self,parent=None):
        super(SignApp, self).__init__(parent)
        QDialog.__init__(self)
        self.setupUi(self)
        self.Handle_Ui()
        self.Handle_Buttons()
    def Handle_Ui(self):
        self.setWindowTitle('Sign up OMR System')
        self.setWindowIcon(QIcon('send-user.png'))

    def Handle_Buttons(self):
        self.pushButton.clicked.connect(self.signup)


    def signup(self):
        email=self.lineEdit.text().strip()
        name=self.lineEdit_2.text().strip()
        password1=self.lineEdit_3.text().strip()
        passwor2=self.lineEdit_4.text().strip()
        if email=='' or name=='' or password1=='' or passwor2=='':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("invalid data")
            msg.setInformativeText("please enter a valid data ")
            msg.setWindowTitle("invalid data")
            retval = msg.exec_()
        else:
            if password1==passwor2:
                db = pymysql.connect("localhost", 'root', '', 'omr')
                sql1=""" SELECT * FROM doctors WHERE email= '{}'  """.format(email)
                cursor = db.cursor()
                cursor.execute(sql1)
                res=cursor.fetchall()
                if len(res)>0:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("invalid data")
                    msg.setInformativeText("username is already exist ")
                    msg.setWindowTitle("invalid data")
                    retval = msg.exec_()
                sql = """INSERT INTO doctors(email,name, password)
                VALUES ('{}', '{}', '{}')""".format(email,name,password1)
                try:
                    cursor1=db.cursor()
                    cursor1.execute(sql)
                    db.commit()
                    db.close()
                    self.main_obj = MainApp()
                    self.hide()
                    self.main_obj.show()
                    self.main_obj.label_4.setText('{}'.format(email))
                except:
                    db.rollback()
                    db.close()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("invalid data")
                msg.setInformativeText("password confirm does not match ")
                msg.setWindowTitle("invalid data")
                retval = msg.exec_()


def main():
    app=QApplication(sys.argv)
    window=SignApp()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()