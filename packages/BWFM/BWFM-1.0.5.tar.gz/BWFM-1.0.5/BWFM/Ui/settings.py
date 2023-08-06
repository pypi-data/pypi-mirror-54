# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BWFM/Ui/settings.ui',
# licensing of 'BWFM/Ui/settings.ui' applies.
#
# Created: Wed Oct 30 22:55:14 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_settingsDialog(object):
    def setupUi(self, settingsDialog):
        settingsDialog.setObjectName("settingsDialog")
        settingsDialog.setWindowModality(QtCore.Qt.NonModal)
        settingsDialog.resize(765, 293)
        settingsDialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(settingsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.warnLabel = QtWidgets.QLabel(settingsDialog)
        self.warnLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.warnLabel.setObjectName("warnLabel")
        self.verticalLayout.addWidget(self.warnLabel)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelBase = QtWidgets.QLabel(settingsDialog)
        self.labelBase.setObjectName("labelBase")
        self.horizontalLayout.addWidget(self.labelBase)
        self.lineBase = QtWidgets.QLineEdit(settingsDialog)
        self.lineBase.setEnabled(False)
        self.lineBase.setPlaceholderText("")
        self.lineBase.setObjectName("lineBase")
        self.horizontalLayout.addWidget(self.lineBase)
        self.pushBase = QtWidgets.QPushButton(settingsDialog)
        self.pushBase.setObjectName("pushBase")
        self.horizontalLayout.addWidget(self.pushBase)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelUpdate = QtWidgets.QLabel(settingsDialog)
        self.labelUpdate.setObjectName("labelUpdate")
        self.horizontalLayout_2.addWidget(self.labelUpdate)
        self.lineUpdate = QtWidgets.QLineEdit(settingsDialog)
        self.lineUpdate.setEnabled(False)
        self.lineUpdate.setObjectName("lineUpdate")
        self.horizontalLayout_2.addWidget(self.lineUpdate)
        self.pushUpdate = QtWidgets.QPushButton(settingsDialog)
        self.pushUpdate.setObjectName("pushUpdate")
        self.horizontalLayout_2.addWidget(self.pushUpdate)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelDLC = QtWidgets.QLabel(settingsDialog)
        self.labelDLC.setObjectName("labelDLC")
        self.horizontalLayout_3.addWidget(self.labelDLC)
        self.lineDLC = QtWidgets.QLineEdit(settingsDialog)
        self.lineDLC.setEnabled(False)
        self.lineDLC.setObjectName("lineDLC")
        self.horizontalLayout_3.addWidget(self.lineDLC)
        self.pushDLC = QtWidgets.QPushButton(settingsDialog)
        self.pushDLC.setObjectName("pushDLC")
        self.horizontalLayout_3.addWidget(self.pushDLC)
        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushOk = QtWidgets.QPushButton(settingsDialog)
        self.pushOk.setObjectName("pushOk")
        self.horizontalLayout_4.addWidget(self.pushOk)
        self.pushCancel = QtWidgets.QPushButton(settingsDialog)
        self.pushCancel.setObjectName("pushCancel")
        self.horizontalLayout_4.addWidget(self.pushCancel)
        self.gridLayout.addLayout(self.horizontalLayout_4, 4, 0, 1, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 1)

        self.retranslateUi(settingsDialog)
        QtCore.QMetaObject.connectSlotsByName(settingsDialog)

    def retranslateUi(self, settingsDialog):
        settingsDialog.setWindowTitle(QtWidgets.QApplication.translate("settingsDialog", "Settings", None, -1))
        self.warnLabel.setText(QtWidgets.QApplication.translate("settingsDialog", "<html><head/><body><p><span style=\" color:#ff0000;\">No changes are ever done to your original game files!</span></p></body></html>", None, -1))
        self.labelBase.setText(QtWidgets.QApplication.translate("settingsDialog", "BOTW Base \'content\' folder: ", None, -1))
        self.pushBase.setText(QtWidgets.QApplication.translate("settingsDialog", "Browse", None, -1))
        self.labelUpdate.setText(QtWidgets.QApplication.translate("settingsDialog", "BOTW Update \'content\' folder: ", None, -1))
        self.lineUpdate.setPlaceholderText(QtWidgets.QApplication.translate("settingsDialog", "optional", None, -1))
        self.pushUpdate.setText(QtWidgets.QApplication.translate("settingsDialog", "Browse", None, -1))
        self.labelDLC.setText(QtWidgets.QApplication.translate("settingsDialog", "BOTW DLC \'content\' folder: ", None, -1))
        self.lineDLC.setPlaceholderText(QtWidgets.QApplication.translate("settingsDialog", "optional", None, -1))
        self.pushDLC.setText(QtWidgets.QApplication.translate("settingsDialog", "Browse", None, -1))
        self.pushOk.setText(QtWidgets.QApplication.translate("settingsDialog", "Ok", None, -1))
        self.pushCancel.setText(QtWidgets.QApplication.translate("settingsDialog", "Cancel", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    settingsDialog = QtWidgets.QDialog()
    ui = Ui_settingsDialog()
    ui.setupUi(settingsDialog)
    settingsDialog.show()
    sys.exit(app.exec_())

