import json
import os
import subprocess
import sys
from pathlib import Path
from time import sleep, time

from PySide2 import QtCore, QtGui, QtWidgets

from BWFM.Ui.about import Ui_aboutDialog
from BWFM.Ui.mainwindow import Ui_MainWindow
from BWFM.Ui.settings import Ui_settingsDialog
from BWFM.util import conf_dir, conf_path


class OVFSError(Exception):
    pass


class CFSError(Exception):
    pass


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        with open(conf_path, "r") as f:
            conf_dict = json.loads(f.read())
        self.rom_folders = [conf_dict["base"], conf_dict["update"], conf_dict["dlc"]]
        self.conf_dict = conf_dict

        self.overlayfs = None
        self.contentfs = None
        self.workdir = None

        self.subprocesses = None
        
        self.defaultStylesheet = self.ui.lineDirMount.styleSheet()

        try:
            self.ui.lineDirMount.setText(self.conf_dict["last_mount_dir"])
            self.ui.lineDirWork.setText(self.conf_dict["last_work_dir"])
        except Exception as e:
            print("{}: {}".format(type(e), str(e)))

        self.ui.pushOpenMount.setEnabled(False)
        self.ui.pushOpenWork.setEnabled(False)
        self.ui.pushRepack.setEnabled(False)

        self.ui.pushMount.clicked.connect(self.buttonMount)
        self.ui.pushRepack.clicked.connect(self.buttonPatch)
        self.ui.pushDirMount.clicked.connect(self.buttonDirMount)
        self.ui.pushDirWork.clicked.connect(self.buttonDirWork)
        self.ui.pushOpenMount.clicked.connect(lambda: self.openDir(self.ui.labelDirMount.text()))
        self.ui.pushOpenWork.clicked.connect(lambda: self.openDir(self.ui.labelDirWork.text()))

        self.ui.actionSettings.triggered.connect(self.showSettings)
        self.ui.actionAbout.triggered.connect(self.showAbout)

        self.show()

    def closeEvent(self, event):
        with open(conf_path, "w") as f:
            f.write(json.dumps(self.conf_dict))
        return super().closeEvent(event)

    def showSettings(self):
        return SettingsDialog(self, self.conf_dict)

    def showAbout(self):
        return AboutDialog(self)

    def openDir(self, path):
        if os.name == "nt":
            os.startfile(path)
        elif os.name =="posix":
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, path])

    def botw_mount(self, base, update=None, dlc=None):
        ovfs_dirs = [i for i in [base, update, dlc] if i]
        ovfs_p = None
        cfs_p = None
        if not ovfs_dirs:
            raise AttributeError("No Game ROM folders were provided")
        temp_dir = Path("/tmp").joinpath("BWFS") \
            if os.name != "nt" else \
                Path.home().joinpath("AppData").joinpath("Local").joinpath("Temp").joinpath("BWFS")
        temp_dir.mkdir(exist_ok=True)

        if len(ovfs_dirs) == 1:
            content_dir = ovfs_dirs[0]
        else:
            ovfs = "botw-overlayfs" if os.name != "nt" else "botw-overlayfs.exe"
            ovfs_temp = "botw-overlayfs-{}".format(time())
            content_dir = Path(temp_dir / ovfs_temp)
            content_dir.mkdir()
            args = [ovfs, *ovfs_dirs, content_dir]
            try:
                ovfs_p = _spawn(args)
            except Exception as e:
                raise OVFSError("{}: {}".format(type(e), str(e)))

        self.overlayfs = content_dir
        self.contentfs = self.ui.lineDirMount.text()
        self.workdir = self.ui.lineDirWork.text()

        cfs = "botw-contentfs" if os.name != "nt" else "botw-contentfs.exe"

        # On Windows WinFsp, the mountpoint must not exist
        if os.name == "nt":
            if Path(self.contentfs).is_dir():
                Path(self.contentfs).rmdir()
        
        if self.workdir:
            args = [cfs, "-w", self.workdir, self.overlayfs, self.contentfs]
        else:
            args = [cfs, self.overlayfs, self.contentfs]

        try:
            cfs_p =_spawn(args)
        except Exception as e:
            raise CFSError("{}: {}".format(type(e), str(e)))

        if ovfs_p:
            return ovfs_p, cfs_p
        else:
            return cfs_p

    def botw_unmount(self):
        for process in self.subprocesses:
            process.terminate()

    def buttonMount(self):
        if self.ui.lineDirMount.text():
            self.ui.lineDirMount.setStyleSheet(self.defaultStylesheet)

            self.ui.pushDirMount.setEnabled(False)
            self.ui.pushDirWork.setEnabled(False)

            self.ui.pushMount.setText("Unmount!")
            self.ui.pushMount.clicked.disconnect()
            self.ui.pushMount.clicked.connect(self.buttonUnmount)

            self.ui.pushOpenMount.setEnabled(True)
            self.ui.pushOpenWork.setEnabled(True)
            self.ui.pushRepack.setEnabled(True)

            self.subprocesses = [self.botw_mount(*self.rom_folders)]
        
            self.conf_dict.update({"last_mount_dir": self.contentfs, "last_work_dir": self.workdir})
        else:
            self.ui.lineDirMount.setStyleSheet("background-color: darkred;")

    def buttonUnmount(self):
        self.ui.pushDirMount.setEnabled(True)
        self.ui.pushDirWork.setEnabled(True)

        self.ui.pushMount.setText("Mount!")
        self.ui.pushMount.clicked.disconnect()
        self.ui.pushMount.clicked.connect(self.buttonMount)

        self.ui.pushOpenMount.setEnabled(False)
        self.ui.pushOpenWork.setEnabled(False)
        self.ui.pushRepack.setEnabled(False)

        self.botw_unmount()

    def buttonPatch(self):
        folder = browse(parent=self, caption="Select directory for repacking")
        if not folder:
            pass
        elif not os.listdir(folder):
            dialog = QtWidgets.QMessageBox.question(
                self,
                "Endianness",
                "Select a console you're making the mod for.\nYes (Wii U)\nNo (Switch)"
            )
            print(dialog)
            if dialog == QtWidgets.QMessageBox.Yes:
                target = "wiiu"
            else:
                target = "switch"
            print(target)
            patcher = "botw-patcher" if os.name != "nt" else "botw-patcher.exe"
            args = [patcher, self.overlayfs, self.workdir, folder, "--force", "--target", target]
            subprocess.run(args, check=True)
            QtWidgets.QMessageBox.information(self, "Done", "Repacking for {} done".format(target))
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "Directory is not empty.")
            self.buttonPatch()

    def buttonDirMount(self):
        folder = browse(self, "Select mount directory")
        if not folder:
            pass
        elif not os.listdir(folder):
            self.ui.lineDirMount.setText(folder)
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Directory is not empty.")
            self.buttonDirMount()

    def buttonDirWork(self):
        folder = browse(self, "Select work directory")
        if not folder:
            pass
        else:
            self.ui.lineDirWork.setText(folder)


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, conf_dict=None):
        super().__init__(parent=parent)
        self.conf_dict = conf_dict
        self.ui = Ui_settingsDialog()
        self.ui.setupUi(self)
        self.defaultStyleSheet = self.ui.lineBase.styleSheet()

        if self.conf_dict:
            self.ui.lineBase.setText(self.conf_dict["base"])
            self.ui.lineUpdate.setText(self.conf_dict["update"])
            self.ui.lineDLC.setText(self.conf_dict["dlc"])

        self.ui.pushBase.clicked.connect(lambda: self.select_dir("Select base game 'content' folder", self.ui.lineBase))
        self.ui.pushUpdate.clicked.connect(lambda: self.select_dir("Select update 'content' folder", self.ui.lineUpdate))
        self.ui.pushDLC.clicked.connect(lambda: self.select_dir("Select DLC 'content' folder", self.ui.lineDLC))
        self.ui.pushCancel.clicked.connect(self.close)
        self.ui.pushOk.clicked.connect(self.ok)

        self.show()

    def select_dir(self, caption, line):
        folder = browse(self, caption)
        if Path(folder).joinpath("System").is_dir():
            line.setText(folder)
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid Game ROM folder.")
            self.select_dir(caption, line)

    def ok(self):
        if not self.ui.lineBase.text():
            self.ui.lineBase.setStyleSheet("background-color: darkred;")
        else:
            conf_dict = {
                "base": self.ui.lineBase.text(),
                "update": self.ui.lineUpdate.text(),
                "dlc": self.ui.lineDLC.text()
            }
            if self.conf_dict != conf_dict:
                with open(conf_path, "w") as f:
                    f.write(json.dumps(conf_dict))
            self.ui.lineBase.setStyleSheet(self.defaultStyleSheet)
            self.accept()


class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_aboutDialog()
        self.ui.setupUi(self)
        self.show()


def browse(parent, caption):
    folder = QtWidgets.QFileDialog.getExistingDirectory(parent=parent, caption="Select a folder", dir=str(Path.home()))
    if not folder:
        pass
    else:
        return folder

# Copied from leoetlino's botwfstools with zero shame
def _spawn(args):
    if os.name == 'nt':
        return subprocess.Popen(args, stdout=subprocess.DEVNULL, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    return subprocess.Popen(args, stdout=subprocess.DEVNULL, preexec_fn=os.setpgrp)


def main():
    app = QtWidgets.QApplication(sys.argv)
    if not conf_path.is_file():
        QtWidgets.QMessageBox.information(
            None,
            "First launch",
            "It looks like it's the first time you're launching BWFM.\
                \nPlease set up your ROM locations in the following window."
        )
        dialog = SettingsDialog(None)
        if dialog.exec_() == SettingsDialog.Accepted:
            window = MainWindow()
            sys.exit(app.exec_())
    else:
        window = MainWindow()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
