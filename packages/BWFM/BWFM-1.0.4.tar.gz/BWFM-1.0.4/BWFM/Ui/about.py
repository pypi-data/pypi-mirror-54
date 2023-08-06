# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BWFM/Ui/about.ui',
# licensing of 'BWFM/Ui/about.ui' applies.
#
# Created: Wed Oct 30 21:36:28 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_aboutDialog(object):
    def setupUi(self, aboutDialog):
        aboutDialog.setObjectName("aboutDialog")
        aboutDialog.resize(330, 82)
        self.gridLayout = QtWidgets.QGridLayout(aboutDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.nameLabel = QtWidgets.QLabel(aboutDialog)
        self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.repoLabel = QtWidgets.QLabel(aboutDialog)
        self.repoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.repoLabel.setOpenExternalLinks(True)
        self.repoLabel.setObjectName("repoLabel")
        self.horizontalLayout.addWidget(self.repoLabel)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(aboutDialog)
        QtCore.QMetaObject.connectSlotsByName(aboutDialog)

    def retranslateUi(self, aboutDialog):
        aboutDialog.setWindowTitle(QtWidgets.QApplication.translate("aboutDialog", "About BWFM", None, -1))
        self.nameLabel.setText(QtWidgets.QApplication.translate("aboutDialog", "Breath of the Wild Filesystem Mounter", None, -1))
        self.repoLabel.setText(QtWidgets.QApplication.translate("aboutDialog", "<html><head/><body><p><a href=\"https://github.com/23kreny/BWFM\"><span style=\" text-decoration: underline; color:#009dff;\">GitHub repository</span></a></p></body></html>", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    aboutDialog = QtWidgets.QDialog()
    ui = Ui_aboutDialog()
    ui.setupUi(aboutDialog)
    aboutDialog.show()
    sys.exit(app.exec_())

