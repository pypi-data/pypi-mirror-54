# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BWFM/Ui/mainwindow.ui',
# licensing of 'BWFM/Ui/mainwindow.ui' applies.
#
# Created: Wed Oct 30 21:36:29 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(626, 469)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelDirMount = QtWidgets.QLabel(self.centralwidget)
        self.labelDirMount.setObjectName("labelDirMount")
        self.horizontalLayout.addWidget(self.labelDirMount)
        self.lineDirMount = QtWidgets.QLineEdit(self.centralwidget)
        self.lineDirMount.setEnabled(False)
        self.lineDirMount.setText("")
        self.lineDirMount.setObjectName("lineDirMount")
        self.horizontalLayout.addWidget(self.lineDirMount)
        self.pushDirMount = QtWidgets.QPushButton(self.centralwidget)
        self.pushDirMount.setObjectName("pushDirMount")
        self.horizontalLayout.addWidget(self.pushDirMount)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelDirWork = QtWidgets.QLabel(self.centralwidget)
        self.labelDirWork.setObjectName("labelDirWork")
        self.horizontalLayout_2.addWidget(self.labelDirWork)
        self.lineDirWork = QtWidgets.QLineEdit(self.centralwidget)
        self.lineDirWork.setEnabled(False)
        self.lineDirWork.setText("")
        self.lineDirWork.setObjectName("lineDirWork")
        self.horizontalLayout_2.addWidget(self.lineDirWork)
        self.pushDirWork = QtWidgets.QPushButton(self.centralwidget)
        self.pushDirWork.setObjectName("pushDirWork")
        self.horizontalLayout_2.addWidget(self.pushDirWork)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushOpenMount = QtWidgets.QPushButton(self.centralwidget)
        self.pushOpenMount.setObjectName("pushOpenMount")
        self.horizontalLayout_3.addWidget(self.pushOpenMount)
        self.pushOpenWork = QtWidgets.QPushButton(self.centralwidget)
        self.pushOpenWork.setObjectName("pushOpenWork")
        self.horizontalLayout_3.addWidget(self.pushOpenWork)
        self.pushMount = QtWidgets.QPushButton(self.centralwidget)
        self.pushMount.setObjectName("pushMount")
        self.horizontalLayout_3.addWidget(self.pushMount)
        self.pushRepack = QtWidgets.QPushButton(self.centralwidget)
        self.pushRepack.setObjectName("pushRepack")
        self.horizontalLayout_3.addWidget(self.pushRepack)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 626, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionSettings)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Breath of the Wild Filesystem Mounter", None, -1))
        self.labelDirMount.setText(QtWidgets.QApplication.translate("MainWindow", "Mount directory: ", None, -1))
        self.pushDirMount.setText(QtWidgets.QApplication.translate("MainWindow", "Browse", None, -1))
        self.labelDirWork.setText(QtWidgets.QApplication.translate("MainWindow", "Work directory: ", None, -1))
        self.lineDirWork.setPlaceholderText(QtWidgets.QApplication.translate("MainWindow", "optional", None, -1))
        self.pushDirWork.setText(QtWidgets.QApplication.translate("MainWindow", "Browse", None, -1))
        self.pushOpenMount.setText(QtWidgets.QApplication.translate("MainWindow", "Open mount directory", None, -1))
        self.pushOpenWork.setText(QtWidgets.QApplication.translate("MainWindow", "Open work directory", None, -1))
        self.pushMount.setText(QtWidgets.QApplication.translate("MainWindow", "Mount!", None, -1))
        self.pushRepack.setText(QtWidgets.QApplication.translate("MainWindow", "Repack modified files", None, -1))
        self.textBrowser.setHtml(QtWidgets.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Noto Sans\';\">Mount directory: Here, you\'ll have access to all files inside archives, no manual unpacking. Files you modify in this folder go inside your work directory.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Noto Sans\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Noto Sans\';\">Work directory: Here, all files you modify/add inside mount directory will be stored. If unfilled, files are mounted in read-only mode.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Noto Sans\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Noto Sans\';\">Fill these, then click \'Mount!\'.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Noto Sans\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Noto Sans\';\">Once you\'re done modding, click \'Repack modified files\' and select a directory of your mod. For WiiU, it is recommended to run the mod through BCML first due to better RSTB calculation and partial pack creation.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Noto Sans\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Noto Sans\'; font-weight:600; color:#ff0004;\">NO ORIGINAL FILES ARE EVER MODIFIED. THE BASE, UPDATE AND DLC FOLDERS ARE SAFE.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Noto Sans\'; font-weight:600; color:#ff0004;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Noto Sans\';\">Known Windows problems:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Noto Sans\';\">Cannot directly duplicate files (copy it elsewhere, then to the mount directory to avoid corruption)</span></p></body></html>", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.menuAbout.setTitle(QtWidgets.QApplication.translate("MainWindow", "Help", None, -1))
        self.actionSettings.setText(QtWidgets.QApplication.translate("MainWindow", "Settings", None, -1))
        self.actionAbout.setText(QtWidgets.QApplication.translate("MainWindow", "About BWMT", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

