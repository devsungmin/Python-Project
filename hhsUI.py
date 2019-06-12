'''
총 지출, 총 수입 구해서 라벨로 넣어주기
만약 그래프를 만들어 주면 카테고리별로 소비 금액을 구한 금액 / 총금액 
'''

import sys
import csv
import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt, QVariant
# from PyQt5.QtWidgets import QWidget, QBoxLayout, QPushButton, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt

class Ui_mainWindow(object):
    #가계부 메인 UI
    def setupUi(self, mainWindow):
        expCat = ['식비', '주거', '통신', '의복', '건강', '교통', '오락', '세금', '기타']
        incCat = ['주수입', '부수입', '기타수입']

        mainWindow.setObjectName("mainWindow")
        mainWindow.setWindowTitle("가계부")
        mainWindow.resize(804, 600)
        mainWindow.setMouseTracking(False) 
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")

    # 달력 UI
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setEnabled(True)
        self.calendarWidget.setGeometry(QtCore.QRect(10, 10, 344, 236))
        self.calendarWidget.setObjectName("calendarWidget")

    # 수입 UI
        self.incLb = QtWidgets.QLabel(self.centralwidget)
        self.incLb.setGeometry(QtCore.QRect(20, 250, 41, 41))
        self.incLb.setObjectName("incLb")
        self.incLb.setText("수입")
        
        self.incComBx = QtWidgets.QComboBox(self.centralwidget)
        self.incComBx.setGeometry(QtCore.QRect(30, 290, 71, 41))
        self.incComBx.setObjectName("incComBx")
        for value in incCat:
            self.incComBx.addItem(value)
        
        self.incLine = QtWidgets.QLineEdit(self.centralwidget)
        self.incLine.setGeometry(QtCore.QRect(120, 290, 131, 41))
        self.incLine.setValidator(QIntValidator(0, 9999999))
        self.incLine.setObjectName("incLine")

        self.won1 = QtWidgets.QLabel(self.centralwidget)
        self.won1.setGeometry(QtCore.QRect(260, 300, 21, 16))
        self.won1.setObjectName("won1")
        self.won1.setText("\\")

        self.incBtn = QtWidgets.QPushButton(self.centralwidget)
        self.incBtn.setGeometry(QtCore.QRect(290, 290, 61, 41))
        self.incBtn.clicked.connect(self.inputInc)
        self.incBtn.setObjectName("incBtn")
        self.incBtn.setText("기입")

    # 지출 UI
        self.expLb = QtWidgets.QLabel(self.centralwidget)
        self.expLb.setGeometry(QtCore.QRect(20, 350, 41, 41))
        self.expLb.setObjectName("expLb")
        self.expLb.setText("지출")

        self.expComBx = QtWidgets.QComboBox(self.centralwidget)
        self.expComBx.setGeometry(QtCore.QRect(30, 390, 71, 41))
        self.expComBx.setObjectName("expComBx")
        for value in expCat:
            self.expComBx.addItem(value)

        self.expLine = QtWidgets.QLineEdit(self.centralwidget)
        self.expLine.setGeometry(QtCore.QRect(120, 390, 131, 41))
        self.expLine.setValidator(QIntValidator(0, 9999999))
        self.expLine.setObjectName("expLine")

        self.won2 = QtWidgets.QLabel(self.centralwidget)
        self.won2.setGeometry(QtCore.QRect(260, 400, 21, 16))
        self.won2.setObjectName("won2")
        self.won2.setText("\\")

        self.expBtn = QtWidgets.QPushButton(self.centralwidget)
        self.expBtn.setGeometry(QtCore.QRect(290, 390, 61, 41))
        self.expBtn.clicked.connect(self.inputExp)
        self.expBtn.setObjectName("expBtn")
        self.expBtn.setText("기입")

        self.explainLb = QtWidgets.QLabel(self.centralwidget)
        self.explainLb.setGeometry(QtCore.QRect(20, 450, 101, 16))
        self.explainLb.setObjectName("explainLb")
        self.explainLb.setText("세부 설명")

        self.expText = QtWidgets.QTextEdit(self.centralwidget)
        self.expText.setGeometry(QtCore.QRect(30, 480, 321, 91))
        self.expText.setObjectName("expText")

    # 이번 달 소비, 지출 금액 합계 UI
        self.totalLb = QtWidgets.QLabel(self.centralwidget)
        self.totalLb.setGeometry(QtCore.QRect(380, 10, 170, 16))
        self.totalLb.setObjectName("totalLb")
        self.totalLb.setText("이번 달 소비 / 지출 합계")

        self.totalExpLb = QtWidgets.QLabel(self.centralwidget)
        self.totalExpLb.setGeometry(QtCore.QRect(410, 40, 250, 16))
        self.totalExpLb.setObjectName("totalExpLb")
        self.totalExpLb.setText("총 지출  ") # 지출 총 합 뒤에 + 로 붙이기

        self.totalIncLb = QtWidgets.QLabel(self.centralwidget)
        self.totalIncLb.setGeometry(QtCore.QRect(410, 140, 250, 16))
        self.totalIncLb.setObjectName("totalIncLb")
        self.totalIncLb.setText("총 수입  ") # 수입 총 합 뒤에 + 로 붙이기

    # 소비, 지출 리스트 UI
        self.listLb = QtWidgets.QLabel(self.centralwidget)
        self.listLb.setGeometry(QtCore.QRect(380, 260, 130, 16))
        self.listLb.setObjectName("listLb")
        self.listLb.setText("수입 / 지출 리스트")

        self.delBtn = QtWidgets.QPushButton(self.centralwidget)
        self.delBtn.setGeometry(QtCore.QRect(710, 250, 61, 41))
        self.delBtn.clicked.connect(self.delList)
        self.delBtn.setObjectName("expBtn")
        self.delBtn.setText("삭제")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(390, 290, 381, 281))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(4)
        self.setTableWidgetData()
        mainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    # 이전에 저장된 csv file load
    def csv_load(self):
        f = open('household_ledger.csv', 'r', encoding = 'utf-8')
        rdr =  csv.reader(f)
        income = 0
        outcome = 0
        for line in rdr:
            self.csv_insertItem(line[1], line[2], line[3], line[4])
            if '수입' in line[2]:
                income += int(line[4])
            elif '지출' in line[2]:
                outcome += int(line[4])
        self.totalIncLb.setText("총 수입: " + str(income))
        self.totalExpLb.setText("총 지출: " + str(outcome))
        f.close()
    
    #테이블에 insert될 때 마다 csv에 한줄 한줄 저장
    def table_to_csv(self, cnt_row, date, inout, category, money):
        f = open("household_ledger.csv", 'a', encoding = "utf-8", newline = '')
        wr = csv.writer(f)
        wr.writerow([cnt_row, date, inout, category, money])
        f.close()

    def csv_insertItem(self, date, inout, category, money):
        cnt_row = self.tableWidget.rowCount()

        self.tableWidget.setItem(cnt_row - 1, 0, QtWidgets.QTableWidgetItem(date))
        self.tableWidget.setItem(cnt_row - 1, 1, QtWidgets.QTableWidgetItem(inout))
        self.tableWidget.setItem(cnt_row - 1, 2, QtWidgets.QTableWidgetItem(category))
        self.tableWidget.setItem(cnt_row - 1, 3, QtWidgets.QTableWidgetItem(money))
        self.tableWidget.setRowCount(cnt_row + 1)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    #수입 지출에 대한 tableInsert
    def insertItem(self, date, inout, category, money):
        cnt_row = self.tableWidget.rowCount()
        
        if "수입" in inout:
            self.table_to_csv(cnt_row, date, inout, category, money)
            self.tableWidget.setItem(cnt_row - 1, 0, QtWidgets.QTableWidgetItem(date))
            self.tableWidget.setItem(cnt_row - 1, 1, QtWidgets.QTableWidgetItem("수입"))
            self.tableWidget.setItem(cnt_row - 1, 2, QtWidgets.QTableWidgetItem(category))
            self.tableWidget.setItem(cnt_row - 1, 3, QtWidgets.QTableWidgetItem(money))
            self.tableWidget.setRowCount(cnt_row + 1)

        elif "지출" in inout:
            self.table_to_csv(cnt_row, date, inout, category, money)                       
            self.tableWidget.setItem(cnt_row - 1, 0, QtWidgets.QTableWidgetItem(date))
            self.tableWidget.setItem(cnt_row - 1, 1, QtWidgets.QTableWidgetItem("지출"))
            self.tableWidget.setItem(cnt_row - 1, 2, QtWidgets.QTableWidgetItem(category))
            self.tableWidget.setItem(cnt_row - 1, 3, QtWidgets.QTableWidgetItem(money))
            self.tableWidget.setRowCount(cnt_row + 1)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    #tableWidget dataInit    
    def setTableWidgetData(self):
        column_headers = ['날짜', '수입/지출', '카테고리', '금액']
        self.tableWidget.setHorizontalHeaderLabels(column_headers)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    # 수입금액 기입을 위한 버튼액션
    def inputInc(self):
        date = self.calendarWidget.selectedDate()
        date = str(date.toString())
        money = str(self.incLine.text()) # 수입금액
        category = str(self.incComBx.currentText()) # 수입 분류
        current_inc = int(str(self.totalIncLb.text()).split(' ')[2])
        print(current_inc)
        current_inc += int(money)
        self.totalIncLb.setText("총 수입: " + str(current_inc))
        self.insertItem(date, "수입", category, money)
        
    # 지출금액 기입을 위한 버튼액션
    def inputExp(self):
        date = self.calendarWidget.selectedDate()
        date = str(date.toString())
        money = str(self.expLine.text()) # 지출 금액
        category = str(self.expComBx.currentText()) # 지출 분
        current_out = int(str(self.totalExpLb.text()).split(' ')[2])
        current_out += int(money)
        self.totalExpLb.setText("총 지출: " + str(current_out))
        self.insertItem(date, "지출", category, money)
        
    # 수입/지출 목록 삭제를 위한 버튼액션
    def delList(self):        
        # print("cnt_row" ,  cnt_row)
        if self.tableWidget.rowCount() > 1:   
            self.tableWidget.removeRow(self.tableWidget.currentRow())
            cnt_row = self.tableWidget.rowCount()
            f = open("household_ledger.csv", 'w', encoding = 'utf-8', newline = '')
            f.close()
            income, outcome = 0, 0
            for i in range(0, cnt_row - 1):
                date = self.tableWidget.item(i, 0).text()
                inout = self.tableWidget.item(i, 1).text()
                category = self.tableWidget.item(i, 2).text()
                money = self.tableWidget.item(i, 3).text()
                if '수입' in inout:
                    income += int(money)
                elif '지출' in inout:
                    outcome += int(money)
                self.table_to_csv(i, date, inout, category, money)

            self.totalIncLb.setText("총 수입: " + str(income))
            self.totalExpLb.setText("총 지출: " + str(outcome))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    ui.csv_load()
    sys.exit(app.exec_())