# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'map_cen_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MapCENDialogBase(object):
    def setupUi(self, MapCENDialogBase):
        MapCENDialogBase.setObjectName("MapCENDialogBase")
        MapCENDialogBase.resize(1150, 780)
        self.tabWidget = QtWidgets.QTabWidget(MapCENDialogBase)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1150, 781))
        self.tabWidget.setMinimumSize(QtCore.QSize(1150, 781))
        self.tabWidget.setMaximumSize(QtCore.QSize(1150, 781))
        self.tabWidget.setBaseSize(QtCore.QSize(1150, 781))
        self.tabWidget.setStyleSheet("QWidget#tab{background-image: url(:/plugins/map_cen/Capture.png)}\n"
"QWidget#tab_2{background-image: url(:/plugins/map_cen/Capture.png)}\n"
"QWidget#tab_3{background-image: url(:/plugins/map_cen/Capture.png)}")
        self.tabWidget.setObjectName("tabWidget")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setStyleSheet("QWidget#tab_2{background-image: url(:/plugins/map_cen/Capture.png)}")
        self.tab_2.setObjectName("tab_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_2.setGeometry(QtCore.QRect(50, 230, 331, 351))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setStyleSheet("QGroupBox#groupBox_2{background-color: rgb(255, 255, 255, 170);}")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox.setGeometry(QtCore.QRect(20, 50, 211, 121))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("color: rgb(13, 13, 13);")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 171, 91))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_2.setEnabled(False)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_3.setEnabled(False)
        self.radioButton_3.setCheckable(True)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout.addWidget(self.radioButton_3)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(10, 0, 181, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(11, 11, 11);")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(20, 200, 91, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(8, 8, 8);")
        self.label_3.setObjectName("label_3")
        self.commandLinkButton_4 = QtWidgets.QCommandLinkButton(self.groupBox_2)
        self.commandLinkButton_4.setGeometry(QtCore.QRect(50, 270, 221, 51))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/map_cen/project.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.commandLinkButton_4.setIcon(icon)
        self.commandLinkButton_4.setIconSize(QtCore.QSize(30, 30))
        self.commandLinkButton_4.setObjectName("commandLinkButton_4")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setGeometry(QtCore.QRect(20, 220, 291, 21))
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_3.setGeometry(QtCore.QRect(550, 670, 211, 41))
        self.groupBox_3.setStyleSheet("QGroupBox#groupBox_3{background-color: rgb(255, 255, 255, 170);}")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.commandLinkButton_5 = QtWidgets.QCommandLinkButton(self.groupBox_3)
        self.commandLinkButton_5.setGeometry(QtCore.QRect(0, 0, 211, 41))
        self.commandLinkButton_5.setStyleSheet("QCommandLinkButton#commandLinkButton_3{background-color: rgb(255, 255, 255, 170);}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/plugins/map_cen/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.commandLinkButton_5.setIcon(icon1)
        self.commandLinkButton_5.setIconSize(QtCore.QSize(30, 20))
        self.commandLinkButton_5.setObjectName("commandLinkButton_5")
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_5.setGeometry(QtCore.QRect(810, 670, 191, 41))
        self.groupBox_5.setStyleSheet("QGroupBox#groupBox_5{background-color: rgb(255, 255, 255, 170);}")
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.commandLinkButton_6 = QtWidgets.QCommandLinkButton(self.groupBox_5)
        self.commandLinkButton_6.setGeometry(QtCore.QRect(0, 0, 191, 41))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/plugins/map_cen/jpg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.commandLinkButton_6.setIcon(icon2)
        self.commandLinkButton_6.setObjectName("commandLinkButton_6")
        self.graphicsView = QtWidgets.QGraphicsView(self.tab_2)
        self.graphicsView.setGeometry(QtCore.QRect(430, 30, 681, 621))
        self.graphicsView.setObjectName("graphicsView")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_4.setGeometry(QtCore.QRect(110, 110, 211, 41))
        self.groupBox_4.setStyleSheet("QGroupBox#groupBox_4{background-color: rgb(255, 255, 255, 170);}")
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.commandLinkButton_2 = QtWidgets.QCommandLinkButton(self.tab_2)
        self.commandLinkButton_2.setGeometry(QtCore.QRect(110, 110, 211, 41))
        self.commandLinkButton_2.setStyleSheet("QCommandLinkButton#commandLinkButton_2{background-color: rgb(255, 255, 255, 170);}")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/plugins/map_cen/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.commandLinkButton_2.setIcon(icon3)
        self.commandLinkButton_2.setIconSize(QtCore.QSize(30, 30))
        self.commandLinkButton_2.setObjectName("commandLinkButton_2")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(110, 640, 211, 71))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/plugins/map_cen/logo.jpg"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.horizontalSlider = QtWidgets.QSlider(self.tab_2)
        self.horizontalSlider.setGeometry(QtCore.QRect(990, 40, 81, 22))
        self.horizontalSlider.setMinimum(-2)
        self.horizontalSlider.setMaximum(2)
        self.horizontalSlider.setSingleStep(6)
        self.horizontalSlider.setProperty("value", 0)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label_9 = QtWidgets.QLabel(self.tab_2)
        self.label_9.setGeometry(QtCore.QRect(960, 40, 21, 21))
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap(":/plugins/map_cen/zoom_out.png"))
        self.label_9.setScaledContents(True)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.tab_2)
        self.label_10.setGeometry(QtCore.QRect(1080, 40, 21, 21))
        self.label_10.setText("")
        self.label_10.setPixmap(QtGui.QPixmap(":/plugins/map_cen/zoom.png"))
        self.label_10.setScaledContents(True)
        self.label_10.setObjectName("label_10")
        self.commandLinkButton_3 = QtWidgets.QCommandLinkButton(self.tab_2)
        self.commandLinkButton_3.setGeometry(QtCore.QRect(1100, 710, 41, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.commandLinkButton_3.setFont(font)
        self.commandLinkButton_3.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/plugins/map_cen/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.commandLinkButton_3.setIcon(icon4)
        self.commandLinkButton_3.setIconSize(QtCore.QSize(25, 25))
        self.commandLinkButton_3.setObjectName("commandLinkButton_3")
        self.mComboBox = QgsCheckableComboBox(self.tab_2)
        self.mComboBox.setGeometry(QtCore.QRect(240, 180, 160, 27))
        self.mComboBox.setObjectName("mComboBox")
        self.graphicsView.raise_()
        self.groupBox_5.raise_()
        self.groupBox_2.raise_()
        self.groupBox_3.raise_()
        self.groupBox_4.raise_()
        self.commandLinkButton_2.raise_()
        self.label_2.raise_()
        self.horizontalSlider.raise_()
        self.label_9.raise_()
        self.label_10.raise_()
        self.commandLinkButton_3.raise_()
        self.mComboBox.raise_()
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_13 = QtWidgets.QLabel(self.tab_3)
        self.label_13.setGeometry(QtCore.QRect(400, 490, 361, 41))
        self.label_13.setText("")
        self.label_13.setPixmap(QtGui.QPixmap(":/plugins/map_cen/onglet.png"))
        self.label_13.setScaledContents(True)
        self.label_13.setObjectName("label_13")
        self.label_11 = QtWidgets.QLabel(self.tab_3)
        self.label_11.setGeometry(QtCore.QRect(310, 130, 531, 411))
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap(":/plugins/map_cen/underconstruction.gif"))
        self.label_11.setScaledContents(True)
        self.label_11.setObjectName("label_11")
        self.label_11.raise_()
        self.label_13.raise_()
        self.tabWidget.addTab(self.tab_3, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_6.setGeometry(QtCore.QRect(680, 350, 141, 41))
        self.groupBox_6.setStyleSheet("QGroupBox#groupBox_6{background-color: rgb(255, 255, 255, 170);}")
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.commandLinkButton = QtWidgets.QCommandLinkButton(self.groupBox_6)
        self.commandLinkButton.setGeometry(QtCore.QRect(0, 0, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.commandLinkButton.setFont(font)
        self.commandLinkButton.setStyleSheet("background-color: qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69));")
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.groupBox_7 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_7.setGeometry(QtCore.QRect(30, 70, 381, 611))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_7.setFont(font)
        self.groupBox_7.setStyleSheet("QGroupBox#groupBox_7{background-color: rgb(255, 255, 255, 170);}")
        self.groupBox_7.setTitle("")
        self.groupBox_7.setObjectName("groupBox_7")
        self.label_4 = QtWidgets.QLabel(self.groupBox_7)
        self.label_4.setGeometry(QtCore.QRect(30, 20, 311, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(11, 11, 11);")
        self.label_4.setObjectName("label_4")
        self.comboBox = QtWidgets.QComboBox(self.groupBox_7)
        self.comboBox.setGeometry(QtCore.QRect(30, 60, 331, 22))
        self.comboBox.setEditable(False)
        self.comboBox.setCurrentText("")
        self.comboBox.setObjectName("comboBox")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_7)
        self.lineEdit_2.setEnabled(True)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 160, 211, 21))
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setReadOnly(False)
        self.lineEdit_2.setClearButtonEnabled(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox_7)
        self.label_6.setGeometry(QtCore.QRect(30, 120, 311, 41))
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(11, 11, 11);")
        self.label_6.setObjectName("label_6")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_7)
        self.lineEdit_3.setEnabled(True)
        self.lineEdit_3.setGeometry(QtCore.QRect(80, 250, 211, 21))
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_3.setReadOnly(False)
        self.lineEdit_3.setClearButtonEnabled(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_7 = QtWidgets.QLabel(self.groupBox_7)
        self.label_7.setGeometry(QtCore.QRect(30, 210, 311, 41))
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(11, 11, 11);")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox_7)
        self.label_8.setGeometry(QtCore.QRect(30, 300, 311, 41))
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(11, 11, 11);")
        self.label_8.setObjectName("label_8")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_7)
        self.lineEdit_4.setEnabled(False)
        self.lineEdit_4.setGeometry(QtCore.QRect(80, 340, 211, 21))
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_4.setReadOnly(False)
        self.lineEdit_4.setClearButtonEnabled(True)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(920, 10, 211, 71))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(":/plugins/map_cen/logo.jpg"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.tabWidget.addTab(self.tab, "")

        self.retranslateUi(MapCENDialogBase)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MapCENDialogBase)

    def retranslateUi(self, MapCENDialogBase):
        _translate = QtCore.QCoreApplication.translate
        MapCENDialogBase.setWindowTitle(_translate("MapCENDialogBase", "MapCEN"))
        self.groupBox.setTitle(_translate("MapCENDialogBase", "Fond de carte"))
        self.radioButton.setText(_translate("MapCENDialogBase", "Orthophotos"))
        self.radioButton_2.setText(_translate("MapCENDialogBase", "OpenStreetMap"))
        self.radioButton_3.setText(_translate("MapCENDialogBase", "Scan 25 IGN"))
        self.label.setText(_translate("MapCENDialogBase", " Préférences de mise en page :"))
        self.label_3.setText(_translate("MapCENDialogBase", "Sites CEN-NA :"))
        self.commandLinkButton_4.setText(_translate("MapCENDialogBase", "  Générer la mise en page"))
        self.lineEdit.setText(_translate("MapCENDialogBase", "Taper le nom du site ici (Ex: Vallée De La Dronne )"))
        self.commandLinkButton_5.setText(_translate("MapCENDialogBase", " Modifier la mise en page"))
        self.commandLinkButton_6.setText(_translate("MapCENDialogBase", "  Exporter en JPEG"))
        self.commandLinkButton_2.setText(_translate("MapCENDialogBase", "Initialisation de MapCEN"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MapCENDialogBase", "Sites CEN et MFU"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MapCENDialogBase", "Connaître / Gérer / Protéger / Valoriser / Accompagner"))
        self.commandLinkButton.setText(_translate("MapCENDialogBase", " Mise en page"))
        self.label_4.setText(_translate("MapCENDialogBase", "Sélectionner un template de mise en page :"))
        self.lineEdit_2.setText(_translate("MapCENDialogBase", "Titre à renseigner ici"))
        self.label_6.setText(_translate("MapCENDialogBase", "Titre de la carte :"))
        self.lineEdit_3.setText(_translate("MapCENDialogBase", "Sous-titre à renseigner ici"))
        self.label_7.setText(_translate("MapCENDialogBase", "Sous-titre de la carte :"))
        self.label_8.setText(_translate("MapCENDialogBase", "Source :"))
        self.lineEdit_4.setText(_translate("MapCENDialogBase", "Automatisable ?"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MapCENDialogBase", "Liste de templates existants"))
from qgscheckablecombobox import QgsCheckableComboBox
import resources_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MapCENDialogBase = QtWidgets.QDialog()
    ui = Ui_MapCENDialogBase()
    ui.setupUi(MapCENDialogBase)
    MapCENDialogBase.show()
    sys.exit(app.exec_())
