from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pymysql
from PyQt5.uic import loadUiType
from os import path
import qdarkstyle
import xlsxwriter
from project import *
import glob
import pandas as pd
import analysis
File=[]
modelImg=[]
Path=[]
excelData=(['seat number','subject name','model number','mark','full mark'],)

FORM_CLASS,s= loadUiType(path.join(path.dirname(__file__),'main.ui'))
class MainApp(QMainWindow,FORM_CLASS):
    def __init__(self,parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Ui()
        self.Handle_Buttons()
        self.model=self.spinBox.value()
    def Handle_Ui(self):
        self.setWindowTitle('Welcome OMR System')
        self.setWindowIcon(QIcon('1.jpeg'))
        label1 = self.label_3
        pixmap1 = QPixmap('1.jpeg')
        label1.setPixmap(pixmap1)
        label1.setScaledContents(True)
        label1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

    def Handle_Buttons(self):
        self.pushButton_2.clicked.connect(self.Browse_1)
        self.pushButton.clicked.connect(self.Browse)
        self.pushButton_9.clicked.connect(self.Browse_2)
        self.pushButton_3.clicked.connect(self.insert_subject)
        self.pushButton_4.clicked.connect(self.evaluation_process)
    def Browse(self):
        place = QFileDialog.getOpenFileName(self, 'BROWSING', 'D:\\the last',
                                            "json files (*.json)")
        Jfile = place[0]
        self.lineEdit_3.setText(Jfile)
    def Browse_1(self):
        place=QFileDialog.getExistingDirectory(self,'BROWSING')
        self.lineEdit_4.setText(place)
    def Browse_2(self):
        place = QFileDialog.getOpenFileName(self, 'BROWSING', 'D:\\the last',
                                            "images JPEG(*.jpg *.jpeg)")
        modelAnswer=place[0]
        self.lineEdit_10.setText(modelAnswer)

    def insert_subject(self):
        name=self.lineEdit_2.text().strip()
        code=self.lineEdit.text().strip()
        modelNumber=self.spinBox.value()
        fullMark = self.spinBox_2.value()
        jsonFile=self.lineEdit_3.text().strip()
        File.append(jsonFile)
        modelAnswer=self.lineEdit_10.text().strip()
        modelImg.append(modelAnswer)
        studentPath=self.lineEdit_4.text().strip()
        Path.append(studentPath)
        if name=='' or code=='' or jsonFile=='' or modelAnswer=='' or studentPath=='':
            self.statusBar().showMessage('please enter a valid data.')
        else:
            db = pymysql.connect("localhost", 'root', '', 'omr')
            sql1 = """ SELECT * FROM subjects WHERE code= '{}'and model={}  """.format(code,modelNumber)
            cursor = db.cursor()
            cursor.execute(sql1)
            res = cursor.fetchall()
            if len(res) > 0:
                self.statusBar().showMessage('model number and subject already exist')
            else:
                user = self.label_4.text()
                sql2= """ SELECT id FROM doctors WHERE email= '{}'  """.format(user)
                cursor1 = db.cursor()
                cursor1.execute(sql2)
                res = cursor1.fetchone()
                Id=res[0]
                sql = """INSERT INTO subjects(code,model, name,fullmark,doctor_id)
                                VALUES ('{}',{},'{}',{},{})""".format(code, modelNumber, name,fullMark,Id)
                try:
                    cursor1 = db.cursor()
                    cursor1.execute(sql)
                    db.commit()
                    db.close()
                    self.statusBar().showMessage('subject inserted successfully')

                except:
                    db.rollback()
                    db.close()

    def evaluation_process(self):
        global excelData
        name=self.lineEdit_2.text().strip()
        code=self.lineEdit.text().strip()
        modelNumber=self.spinBox.value()
        fullMark = self.spinBox_2.value()
        jsonFile=self.lineEdit_3.text().strip()
        modelAnswer=self.lineEdit_10.text().strip()
        studentPath=self.lineEdit_4.text().strip()
        if name=='' or code=='' or jsonFile=='' or modelAnswer=='' or studentPath=='':
            self.statusBar().showMessage('please enter a valid data and click go on first')
        else:
            model_obj = Answer(modelImg[0], File[0])
            s, m, answerKey = model_obj.get_answers()
            myPath=os.path.join(Path[0],'{}\\*.jpeg'.format(Path[0]))
            db=pymysql.connect('localhost','root','','omr')

            for img in glob.glob(myPath):
                student_obj=Answer(img,File[0])
                seat,modelNum,answer=student_obj.get_answers()
                mark=student_obj.evaluate(answer,answerKey)
                db = pymysql.connect('localhost', 'root', '', 'omr')
                sql = """INSERT INTO students(code,model, seatnumber,mark)
                                                VALUES ('{}',{},'{}',{})""".format(str(code), modelNumber, str(seat), mark)
                try:
                    cursor = db.cursor()
                    cursor.execute(sql)
                    db.commit()
                    db.close()
                except:
                    db.rollback()
                    db.close()
                rows=[seat,name,modelNumber,mark,fullMark]
                excelData= excelData+(rows,)
                print(seat,mark)
            self.writer()
        currdir=os.getcwd()
        os.chdir(currdir)
        excel_file='{}{}{}.xlsx'.format(name,code,modelNumber)
        mark_sheet1 = pd.read_excel(excel_file, sheetname=0, index_col=0)
        summary = mark_sheet1['mark'].describe()
        summary.to_excel('{}{}{}analysis.xlsx'.format(name, code, modelNumber))
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(2)
        for row_number,row_data in enumerate(summary.index):
            self.tableWidget_2.insertRow(row_number)
            self.tableWidget_2.setItem(row_number,0,QTableWidgetItem(str(row_data)))
        for row_number,row_data in enumerate(summary):
            self.tableWidget_2.setItem(row_number,1,QTableWidgetItem(str(row_data)))

        self.tableWidget_3.setColumnCount(2)
        failed=analysis.get_failed(code,modelNumber)
        self.tableWidget_3.insertRow(0)
        self.tableWidget_3.setItem(0, 0, QTableWidgetItem('failed'))
        self.tableWidget_3.setItem(0, 1, QTableWidgetItem(str(failed)))
        passed=analysis.get_passed(code,modelNumber)
        self.tableWidget_3.insertRow(1)
        self.tableWidget_3.setItem(1, 0, QTableWidgetItem('passed'))
        self.tableWidget_3.setItem(1, 1, QTableWidgetItem(str(passed)))
        full=analysis.get_full_mark(code,modelNumber)
        self.tableWidget_3.insertRow(2)
        self.tableWidget_3.setItem(2, 0, QTableWidgetItem('full'))
        self.tableWidget_3.setItem(2, 1, QTableWidgetItem(str(full)))

    def writer(self):
        subjectName=self.lineEdit_2.text().strip()
        code=self.lineEdit.text().strip()
        modelNumber=self.spinBox.value()
        workbook = xlsxwriter.Workbook('{}{}{}.xlsx'.format(subjectName,code,modelNumber))
        worksheet = workbook.add_worksheet()
        row = 0
        col = 0
        for seat,name,modelNumber,mark,fullMark in (excelData):
            worksheet.write(row, col, seat)
            worksheet.write(row, col + 1, name)
            worksheet.write(row, col + 2, modelNumber)
            worksheet.write(row, col + 3, mark)
            worksheet.write(row, col + 4, fullMark)
            row += 1
        for row_number,row_data in enumerate(excelData):
            self.tableWidget.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.tableWidget.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        workbook.close()
        self.statusBar().showMessage('evaluation process done,results in result tab')







def main():
    app=QApplication(sys.argv)
    window=MainApp()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()