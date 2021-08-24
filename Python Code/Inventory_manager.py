from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

import sys
from os import path
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller"""
    base_path=getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path,relative_path)


from PyQt5.uic import loadUiType

FORM_CLASS,_=loadUiType(resource_path("main.ui"))

import sqlite3


class Main(QMainWindow, FORM_CLASS):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()
        self.NAVIGATE()

    def Handle_Buttons(self):
        self.refresh_btn.clicked.connect(self.GET_DATA)
        self.search_btn.clicked.connect(self.SEARCH)
        self.check_btn.clicked.connect(self.LEVEL)
        self.update_btn.clicked.connect(self.UPDATE)
        self.delete_btn.clicked.connect(self.DELETE)
        self.add_btn.clicked.connect(self.ADD)
        self.first_btn.clicked.connect(self.FIRST)
        self.previous_btn.clicked.connect(self.PREVIOUS)
        self.next_btn.clicked.connect(self.NEXT)
        self.last_btn.clicked.connect(self.LAST)
        self.darkbutton.clicked.connect(self.DARK)
        self.lightbutton.clicked.connect(self.LIGHT)

    def GET_DATA(self):
        self.NAVIGATE()
        self.count_filter_txt.setValue(0)
        db=sqlite3.connect(resource_path("database.db"))
        cursor=db.cursor()
        command='''SELECT * from parts_table'''
        result=cursor.execute(command)
        self.table.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))

        cursor2=db.cursor()
        cursor3=db.cursor()
        parts_no=''' SELECT COUNT (DISTINCT Partname) from parts_table'''
        ref_no=''' SELECT COUNT (DISTINCT Reference) from parts_table'''
        results_ref_no=cursor2.execute(ref_no)
        results_parts_no=cursor3.execute(parts_no)
        self.ReferenceLabel.setText(str(results_ref_no.fetchone()[0]))
        self.PartsLabel.setText(str(results_parts_no.fetchone()[0]))
        cursor4=db.cursor()
        cursor5=db.cursor()
        min_hole=''' SELECT MIN(NumberOfHoles), Reference from parts_table'''
        max_hole=''' SELECT MAX(NumberOfHoles), Reference from parts_table'''
        results_min_hole=cursor4.execute(min_hole)
        results_max_hole=cursor5.execute(max_hole)
        r1=results_min_hole.fetchone()
        r2=results_max_hole.fetchone()
        self.MinHolesLabel.setText(str(r1[0]))
        self.MaxHolesLabel.setText(str(r2[0]))
        self.REF1.setText(str(r1[1]))
        self.REF2.setText(str(r2[1]))


    def SEARCH(self):
        db=sqlite3.connect(resource_path("database.db"))
        cursor=db.cursor()
        number=int(self.count_filter_txt.text())
        command='''SELECT * from parts_table WHERE count<=?'''
        result=cursor.execute(command,[number])
        self.table.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))

    def LEVEL(self):
        db=sqlite3.connect(resource_path("database.db"))
        cursor=db.cursor()
        command='''SELECT Reference,Partname,Count from parts_table order by Count asc LIMIT 5'''
        result=cursor.execute(command)
        self.table2.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table2.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table2.setItem(row_number,column_number,QTableWidgetItem(str(data)))

    def NAVIGATE(self):
        db=sqlite3.connect(resource_path("database.db"))
        cursor=db.cursor()
        command=''' SELECT * from parts_table'''
        result=cursor.execute(command)
        val=result.fetchone()
        self.id.setText(str(val[0]))
        self.reference.setText(str(val[1]))
        self.part_name.setText(str(val[2]))
        self.min_area.setText(str(val[3]))
        self.max_area.setText(str(val[4]))
        self.no_of_holes.setText(str(val[5]))
        self.min_diameter.setText(str(val[6]))
        self.max_diameter.setText(str(val[7]))
        self.count.setValue(val[8])

    def UPDATE(self):
        db=sqlite3.connect(resource_path("database.db"))
        cursor=db.cursor()
        
        id_=int(self.id.text())
        reference_=self.reference.text()
        part_name_=self.part_name.text()
        min_area_=self.min_area.text()
        max_area_=self.max_area.text()
        no_of_holes_=self.no_of_holes.text()
        min_diameter_=self.min_diameter.text()
        max_diameter_=self.max_diameter.text()
        count_=self.count.value()

        row=(reference_,part_name_,min_area_,max_area_,no_of_holes_,min_diameter_,max_diameter_,count_,id_)

        command=''' UPDATE parts_table SET Reference=?,PartName=?,MinArea=?,MaxArea=?,NumberOfHoles=?,MinDiameter=?,MaxDiameter=?,Count=? WHERE ID=?'''

        cursor.execute(command,row)
        db.commit()



    def DELETE(self):
        db=sqlite3.connect(resource_path("database.db"))
        cursor=db.cursor()

        d=self.id.text()
        command='''DELETE FROM parts_table WHERE ID=?'''
        cursor.execute(command,d)
        db.commit() 

    def ADD(self):
        db=sqlite3.connect(resource_path("database.db"))
        cursor=db.cursor()

        reference_=self.reference.text()
        part_name_=self.part_name.text()
        min_area_=self.min_area.text()
        max_area_=self.max_area.text()
        no_of_holes_=self.no_of_holes.text()
        min_diameter_=self.min_diameter.text()
        max_diameter_=self.max_diameter.text()
        count_=self.count.value()

        row=(reference_,part_name_,min_area_,max_area_,no_of_holes_,min_diameter_,max_diameter_,count_)

        command=''' INSERT INTO parts_table (Reference,PartName,MinArea,MaxArea,NumberOfHoles,MinDiameter,MaxDiameter,Count) VALUES (?,?,?,?,?,?,?,?)'''

        cursor.execute(command,row)
        db.commit()

    
    def FIRST(self):
        db=sqlite3.connect(resource_path("database.db"))
        cursor=db.cursor()
        command='''SELECT * from parts_table order by ID asc LIMIT 1'''
        result=cursor.execute(command)
        val=result.fetchone()
        self.id.setText(str(val[0]))
        self.reference.setText(str(val[1]))
        self.part_name.setText(str(val[2]))
        self.min_area.setText(str(val[3]))
        self.max_area.setText(str(val[4]))
        self.no_of_holes.setText(str(val[5]))
        self.min_diameter.setText(str(val[6]))
        self.max_diameter.setText(str(val[7]))
        self.count.setValue(val[8])
    
    def PREVIOUS(self):
        d=self.id.text()
        db=sqlite3.connect(resource_path("database.db"))
        cursor=db.cursor()
        checkcursor=db.cursor()
        checkcommand='''SELECT ID from parts_table order by ID asc LIMIT 1'''
        checkresult=checkcursor.execute(checkcommand)
        minId=checkresult.fetchone()
        if int(d)==int(minId[0]):
            command='''SELECT * from parts_table order by ID asc LIMIT 1'''
            result=cursor.execute(command)
        else:
            command='''SELECT * from parts_table WHERE ID<? order by ID desc LIMIT 1'''
            result=cursor.execute(command,[d])
        val=result.fetchone()
        self.id.setText(str(val[0]))
        self.reference.setText(str(val[1]))
        self.part_name.setText(str(val[2]))
        self.min_area.setText(str(val[3]))
        self.max_area.setText(str(val[4]))
        self.no_of_holes.setText(str(val[5]))
        self.min_diameter.setText(str(val[6]))
        self.max_diameter.setText(str(val[7]))
        self.count.setValue(val[8])
    
    def NEXT(self):
        d=self.id.text()
        db=sqlite3.connect(resource_path("database.db"))
        cursor=db.cursor()
        checkcursor=db.cursor()
        checkcommand='''SELECT ID from parts_table order by ID desc LIMIT 1'''
        checkresult=checkcursor.execute(checkcommand)
        minId=checkresult.fetchone()
        if int(d)==int(minId[0]):
            command='''SELECT * from parts_table order by ID desc LIMIT 1'''
            result=cursor.execute(command)
        else:
            command=''' SELECT * from parts_table WHERE ID>? order by ID asc LIMIT 1 '''
            result=cursor.execute(command,[d])
        val=result.fetchone()
        self.id.setText(str(val[0]))
        self.reference.setText(str(val[1]))
        self.part_name.setText(str(val[2]))
        self.min_area.setText(str(val[3]))
        self.max_area.setText(str(val[4]))
        self.no_of_holes.setText(str(val[5]))
        self.min_diameter.setText(str(val[6]))
        self.max_diameter.setText(str(val[7]))
        self.count.setValue(val[8])
    
    def LAST(self):
        db=sqlite3.connect(resource_path("database.db"))
        cursor=db.cursor()
        command='''SELECT * from parts_table order by ID desc LIMIT 1'''
        result=cursor.execute(command)
        val=result.fetchone()
        self.id.setText(str(val[0]))
        self.reference.setText(str(val[1]))
        self.part_name.setText(str(val[2]))
        self.min_area.setText(str(val[3]))
        self.max_area.setText(str(val[4]))
        self.no_of_holes.setText(str(val[5]))
        self.min_diameter.setText(str(val[6]))
        self.max_diameter.setText(str(val[7]))
        self.count.setValue(val[8])

    def DARK(self):
        sshFile=resource_path("darkTheme.stylesheet")
        with open(sshFile,"r") as fh:
            self.setStyleSheet(fh.read())

    def LIGHT(self):
        self.setStyleSheet("")

    


def main():
    app=QApplication(sys.argv)
    Window=Main()
    Window.show()
    app.exec_()

if __name__=="__main__":
    main()
