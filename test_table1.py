# Form implementation generated from reading ui file 'test_table.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(782, 315)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(530, 120, 101, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(530, 170, 101, 31))
        self.label_4.setObjectName("label_4")
        self.Count = QtWidgets.QLineEdit(Form)
        self.Count.setGeometry(QtCore.QRect(650, 70, 121, 31))
        self.Count.setObjectName("Count")
        self.Table = QtWidgets.QTableWidget(Form)
        self.Table.setGeometry(QtCore.QRect(20, 20, 491, 281))
        self.Table.setObjectName("Table")
        self.Table.setColumnCount(0)
        self.Table.setRowCount(0)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(530, 20, 101, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(530, 70, 101, 31))
        self.label_2.setObjectName("label_2")
        self.Diam = QtWidgets.QLineEdit(Form)
        self.Diam.setGeometry(QtCore.QRect(650, 170, 121, 31))
        self.Diam.setObjectName("Diam")
        self.AddBtn = QtWidgets.QPushButton(Form)
        self.AddBtn.setGeometry(QtCore.QRect(530, 260, 241, 41))
        self.AddBtn.setObjectName("AddBtn")
        self.Thread = QtWidgets.QComboBox(Form)
        self.Thread.setGeometry(QtCore.QRect(650, 21, 121, 31))
        self.Thread.setObjectName("Thread")
        self.Class = QtWidgets.QComboBox(Form)
        self.Class.setGeometry(QtCore.QRect(650, 120, 121, 31))
        self.Class.setObjectName("Class")
        self.ThrBolt = QtWidgets.QRadioButton(Form)
        self.ThrBolt.setGeometry(QtCore.QRect(540, 230, 95, 20))
        self.ThrBolt.setObjectName("ThrBolt")
        self.PinBolt = QtWidgets.QRadioButton(Form)
        self.PinBolt.setGeometry(QtCore.QRect(660, 230, 95, 20))
        self.PinBolt.setObjectName("PinBolt")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "класс прочности"))
        self.label_4.setText(_translate("Form", "Диаметр отверстия"))
        self.label.setText(_translate("Form", "резьба"))
        self.label_2.setText(_translate("Form", "количество"))
        self.AddBtn.setText(_translate("Form", "Добавить"))
        self.ThrBolt.setText(_translate("Form", "Проходной"))
        self.PinBolt.setText(_translate("Form", "Призонный"))
