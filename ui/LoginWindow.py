from aqt.utils import showInfo
from aqt.qt import (
    QWidget,
    QLineEdit,
    QVBoxLayout,
    QPushButton
)


class LoginWindow(QWidget):

    def __init__(self, mainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()

        self.emailAddress = QLineEdit()
        self.emailAddress.setPlaceholderText('Email Address')
        layout.addWidget(self.emailAddress)

        self.password = QLineEdit()
        self.password.setPlaceholderText('Password')
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.loginButton = QPushButton('Login')
        layout.addWidget(self.loginButton)

        self.loginButton.clicked.connect(self.try_login)

        self.setFixedSize(260, 160)
        self.setLayout(layout)
        self.setWindowTitle('S4C Anki - Login')
        self.show()

    def try_login(self):
        try:
            self.mainWindow.api.login(
                self.emailAddress.text(),
                self.password.text(),
            )
            self.mainWindow.updateLoginSpecificWidgets()
            self.mainWindow.retranslateUi()
            self.close()
        except ValueError:
            showInfo('Email/Password provided was incorrect')
