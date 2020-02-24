import pandas as pd
import xlrd
import pymysql

# excel_file='c++cs1001.xlsx'
# movies_sheet1 = pd.read_excel(excel_file, sheetname=0, index_col=0)
# summary=movies_sheet1['mark'].describe()
# for i,j in enumerate(summary):
#     print(i,j)
#
# summary.to_excel('analysis.xlsx')

def get_failed(code,model):
    db = pymysql.connect('localhost', 'root', '', 'omr')
    cmd = """ SELECT count(seatnumber) as ' failed'
            FROM `students` JOIN `subjects`
            ON students.code=subjects.code
            and students.model = students.model
            WHERE students.code='{}' and students.model={} and mark <= (subjects.fullmark/2)""".format(code,model)
    cursor = db.cursor()
    cursor.execute(cmd)
    res = cursor.fetchone()
    if len(res) > 0:
        return res[0]
    else:
        return  "no one failed"

def get_passed(code,model):
    db = pymysql.connect('localhost', 'root', '', 'omr')
    cmd = """ SELECT count(seatnumber) as ' failed'
            FROM `students` JOIN `subjects`
            ON students.code=subjects.code
            and students.model = students.model
            WHERE students.code='{}' and students.model={} and mark >= (subjects.fullmark/2)""".format(code,model)
    cursor = db.cursor()
    cursor.execute(cmd)
    res = cursor.fetchone()
    if len(res) > 0:
        return res[0]
    else:
        return  "no one passed"

def get_full_mark(code,model):
    db = pymysql.connect('localhost', 'root', '', 'omr')
    cmd = """ SELECT count(seatnumber) as ' failed'
            FROM `students` JOIN `subjects`
            ON students.code=subjects.code
            and students.model = students.model
            WHERE students.code='{}' and students.model={} and mark = subjects.fullmark""".format(code,model)
    cursor = db.cursor()
    cursor.execute(cmd)
    res = cursor.fetchone()
    if len(res) > 0:
        return res[0]
    else:
        return  "no one"


passed=get_passed('cs100',1)
print(passed)