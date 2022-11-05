import os
from PyQt5 import QtWidgets, uic ,QtCore
from ytDownloadClass import ytDownloadClass
from PyQt5.QtGui import QMovie
import sys
import GLBvar
from pathlib import Path
import shutil


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(resource_path('MainView.ui'), self) # Load the .ui file
        GLBvar.init()

        if os.path.exists(str(Path.home() / "tmp")):
            shutil.rmtree(str(Path.home() / "tmp"))
        self.tmpDir = os.mkdir(mode=777,path=str(Path.home() / "tmp"))
        GLBvar.tmpDir = str(Path.home() / "tmp")

        self.button = self.findChild(QtWidgets.QPushButton, 'okBtn') # Find the button
        self.browse = self.findChild(QtWidgets.QPushButton, 'Browse') # Find the button
        GLBvar.downloadBtn = self.findChild(QtWidgets.QPushButton, 'DownloadBtn') # Find the button
        GLBvar.QualityGroup = self.findChild(QtWidgets.QGroupBox,"groupBox_2")
        self.path = str(Path.home() / "Downloads")

        self.ytLink = self.findChild(QtWidgets.QLineEdit, 'ytLink')
        self.ytLink.textChanged.connect(self.reset)
        self.yttype = "mp4" if self.findChild(QtWidgets.QRadioButton, 'MP4').isChecked() else "mp3"

        GLBvar.descLabel = self.findChild(QtWidgets.QLabel, 'desc')
        GLBvar.imgViewer = self.findChild(QtWidgets.QLabel, 'imageViewer')
        self.pathLbl = self.findChild(QtWidgets.QLabel, 'path')
        GLBvar.status = self.findChild(QtWidgets.QLabel, 'status')

        self.mp4 = self.findChild(QtWidgets.QRadioButton, 'MP4')
        self.mp4.toggled.connect(self.changeType)

        self.pathLbl.setText(str(Path.home() / "Downloads"))
        self.button.clicked.connect(self.okBtnAction)
        self.browse.clicked.connect(self.Browse_Path)
        GLBvar.downloadBtn.clicked.connect(self.DownloadBtnAction)
        self.dialog_box = QtWidgets.QMessageBox()

        #preparing loading GIF
        GLBvar.loading_movie = QMovie(resource_path("loading.gif"))
        GLBvar.loading_label = self.findChild(QtWidgets.QLabel, 'loading')
        GLBvar.loading_label.setMovie(GLBvar.loading_movie)
        GLBvar.loading_label.setHidden(True)

        self.show() # Show the GUI

    def changeType(self):
        self.yttype = "mp4" if self.findChild(QtWidgets.QRadioButton, 'MP4').isChecked() else "mp3"


    def getSelectedQuality(self):
        for i in GLBvar.QualityGroup.children() :
            if i.isChecked() :
                return i.text()

    def DownloadBtnAction(self):
        if self.yttype == "mp3":
            GLBvar.yt.Download_MP3(self.path)
        else:
            qlt = self.getSelectedQuality()
            if qlt == None :
                #Error Select Quality
                self.dialog_box.warning(self, "Notice", "\n         Please Select Quality       " )
            else :
                GLBvar.yt.Download_MP4(qlt,self.path)


    def reset(self):
        GLBvar.downloadBtn.setEnabled(False)
        GLBvar.descLabel.setText("")
        GLBvar.imgViewer.clear()
        GLBvar.status.setText("")
        for i in GLBvar.QualityGroup.children() :
            i.setEnabled(False)

    def okBtnAction(self):
        self.reset()
        link = self.ytLink.text()
        try :
            GLBvar.yt = ytDownloadClass(link,self.yttype)
        except:
            self.dialog_box.warning(self, "Notice", "\n         Link Invalid !                 ")
            GLBvar.status.setText("Link Invalid !")
            return
        GLBvar.yt.desc()

        if self.yttype == "mp4" :
            GLBvar.downloadBtn.setEnabled(False)
            GLBvar.yt.get_Quality()


    
    def Browse_Path(self):
        downloads_path = str(Path.home() / "Downloads")
        dialog = QtWidgets.QFileDialog(self, 'Audio Files', downloads_path, "")
        dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        dialog.setSidebarUrls([QtCore.QUrl.fromLocalFile(downloads_path)])
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.pathLbl.setText(str(dialog.selectedFiles()[0]))
            self.path = str(dialog.selectedFiles()[0])
            return 0
        self.pathLbl.setText(downloads_path)
        self.path = downloads_path
        return 0
    
    def __del__(self):
        del GLBvar.yt
        os.remove(f'{GLBvar.tmpDir}\\audio.mp3')
        os.remove(f'{GLBvar.tmpDir}\\video.mp4')
        os.rmdir(str(Path.home() / "tmp"))
    
app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application