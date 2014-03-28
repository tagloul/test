import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.phonon import Phonon

class Icon(QtGui.QWidget):
    """ this class is needed to initialize a icon  and show it on the window
    the init method already opens a window"""
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QtGui.QIcon('Darth-Vader-icon.png'))


class Tooltip(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Tooltip')

        self.setToolTip('This is a <b>QWidget</b> widget')
        QtGui.QToolTip.setFont(QtGui.QFont('OldEnglish', 10))

class QuitButton(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Quit Button')

        quit = QtGui.QPushButton('Close', self)  # self is the object where the button is going to be
        quit.setGeometry(10, 10, 60, 35)

        self.connect(quit, QtCore.SIGNAL('clicked()'),
                     QtGui.qApp, QtCore.SLOT('quit()'))


class MessageBox(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('message box')
        self.media = Phonon.MediaObject(self)
        self.media.stateChanged.connect(self.handleStateChanged)
        self.video = Phonon.VideoWidget(self)
        self.video.setMinimumSize(400, 400)
        #self.audio = Phonon.AudioOutput(Phonon.VideoCategory, self)
        #Phonon.createPath(self.media, self.audio)
        Phonon.createPath(self.media, self.video)
        self.button = QtGui.QPushButton(self.handleButton)
        self.list = QtGui.QListWidget(self)
        self.list.addItems(Phonon.BackendCapabilities.availableMimeTypes())
        layout.addWidget(self.video, 1)
        layout.addWidget(self.button)
        layout.addWidget(self.list)
        
    def handleButton(self):
        if self.media.state() == Phonon.PlayingState:
            self.media.stop()
        else:
            path = QtGui.QFileDialog.getOpenFileName(self, self.button.text())
            if path:
                self.media.setCurrentSource(Phonon.MediaSource(path))
                self.media.play()
    
    def handleStateChanged(self, newstate, oldstate):
        if newstate == Phonon.PlayingState:
            self.button.setText('Stop')
        elif (newstate != Phonon.LoadingState and
              newstate != Phonon.BufferingState):
            self.button.setText('Choose File')
            if newstate == Phonon.ErrorState:
                source = self.media.currentSource().FileName()
                print('ERROR: could not play:', source.toLocal8Bit().data())
                print(' %s' % self.media.errorString().toLocal8Bit().data())

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()



app = QtGui.QApplication(sys.argv)
#sets up a window with icon
#icon = Icon()
#icon.show()
# sets up a window with a tooltip
#tooltip = Tooltip()
#tooltip.show()
qb1 = QuitButton()
qb1.show()
qb1.setWindowIcon(QtGui.QIcon('Darth-Vader-icon.png'))

qb = MessageBox()
qb.show()
qb.setWindowIcon(QtGui.QIcon('Darth-Vader-icon.png'))

# this block opens a small window with title 'simple' in the center of the screen
#===============================================================================
# widget = QtGui.QWidget()
# widget.resize(250, 150)
# widget.setWindowTitle('simple')
#
# widget.setWindowIcon(QtGui.QIcon('Darth-Vader-icon.png'))
# widget.setToolTip("This is a <b>QWidget</b> widget")
# QtGui.QToolTip.setFont(QtGui.QFont('OldEnglish', 10))
#
# widget.show()
#===============================================================================



sys.exit(app.exec_())


print('hello world')
