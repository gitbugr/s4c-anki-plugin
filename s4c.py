from aqt import mw
from .api.api import API
from aqt.qt import (
    QAction
)
from .ui.MainWindow import MainWindow


def setupS4CWindow():
    api = API()
    mw.mainWindow = mainWindow = MainWindow(api)
    mainWindow.show()


action = QAction('Generate Cards from S4C', mw)
action.triggered.connect(setupS4CWindow)
mw.form.menuTools.addAction(action)
