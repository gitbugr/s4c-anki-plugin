from ..utils.debounce import Debounce
from .LoginWindow import LoginWindow
# from aqt.utils import showInfo
from aqt.qt import (
    Qt,
    QSize,
    QRect,
    QFont,
    QLabel,
    QWidget,
    QGroupBox,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QRadioButton,
    QApplication,
    QCoreApplication
)

from .ListingWidget import ListingWidget


class MainWindow(QMainWindow):
    listings = []
    __listings = []

    def __init__(self, api):
        super().__init__()
        self.api = api
        self.initUi()

    def initUi(self):
        self.resize(600, 430)
        self.setMinimumSize(QSize(600, 430))
        self.setMaximumSize(QSize(600, 430))

        debounce = Debounce()

        def startSearch():
            self.loading.show()
            debounce.debounce(self.search, 2000)()

        self.searchBox = QLineEdit(None, self)
        self.searchBox.setGeometry(QRect(200, 20, 381, 21))
        self.searchBox.textChanged.connect(startSearch)

        self.initCardTypeWidget()
        self.initIsLoggedInWidgets()
        self.initIsNotLoggedInWidgets()
        self.updateLoginSpecificWidgets()

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setGeometry(QRect(200, 60, 381, 351))
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 379, 349))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.loading = QLabel(self)
        self.loading.setGeometry(QRect(520, 20, 61, 20))
        self.loading.setFont(font)
        self.loading.setAlignment(Qt.AlignCenter)
        self.loading.hide()

        self.retranslateUi()

    def search(self, *kwargs, **args):
        text = self.searchBox.text()
        self.listings = []
        # remove existing listings
        for listing in self.__listings:
            listing.deleteLater()
        self.__listings = []

        if (text != ''):
            progs = self.api.search_programmes(text)[:20]
            for prog in progs:
                fullProg = self.api.full_programme_info(prog['programme_id'])
                prog['subtitle_e'] = fullProg['subtitle_e']
                prog['subtitle_c'] = fullProg['subtitle_c']
                prog['mpg'] = fullProg['mpg']
                prog['other_progs_in_series'] = (
                    fullProg['other_progs_in_series'] if (
                        hasattr(fullProg, 'other_progs_in_series')
                    ) else []
                )
                if (
                    prog['subtitle_e'] is not None
                    and prog['subtitle_c'] is not None
                ):
                    self.listings.append(prog)
                    self.updateListingsInScrollArea()
                    self.scrollAreaWidgetContents.update()
                    self.scrollArea.update()

            if (len(progs) == 0):
                self.loading.hide()
                self.scrollAreaWidgetContents.update()
                self.scrollArea.update()

    def initCardTypeWidget(self):
        self.cardTypeGroup = QGroupBox(None, self)
        self.cardTypeGroup.setGeometry(QRect(20, 290, 161, 121))

        self.includeVideo = QRadioButton(self.cardTypeGroup)
        self.includeVideo.setGeometry(QRect(10, 30, 141, 20))

        self.includeAudio = QRadioButton(self.cardTypeGroup)
        self.includeAudio.setGeometry(QRect(10, 60, 141, 20))

        self.textOnly = QRadioButton(self.cardTypeGroup)
        self.textOnly.setGeometry(QRect(10, 90, 141, 20))

    def initIsLoggedInWidgets(self):
        self.logged_in_label = QLabel(None, self)
        self.logged_in_label.setObjectName('logged_in_label')
        self.logged_in_label.setGeometry(QRect(20, 20, 161, 16))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.logged_in_label.setFont(font)

        self.logged_in_label_2 = QLabel(None, self)
        self.logged_in_label_2.setObjectName('logged_in_label_2')
        self.logged_in_label_2.setGeometry(QRect(20, 40, 161, 16))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setWeight(50)
        font1.setKerning(True)
        self.logged_in_label_2.setFont(font1)
        self.logged_in_label_2.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )
        self.logged_in_label_2.setWordWrap(True)

        self.logoutButton = QPushButton(None, self)
        self.logoutButton.setObjectName('logoutButton')
        self.logoutButton.setGeometry(QRect(70, 60, 111, 30))
        self.logoutButton.clicked.connect(self.logout)

    def updateListingsInScrollArea(
            self
    ):
        QCoreApplication.processEvents()
        # appends new listings
        for index, listing in enumerate(self.listings):
            listingWidget = ListingWidget(
                self.scrollAreaWidgetContents,
                listing,
                self
            )
            listingWidget.setGeometry(QRect(10, index * 100, 360, 100))
            self.__listings.append(listingWidget)
            QCoreApplication.processEvents()

        listingCount = len(self.listings) - 1

        self.scrollAreaWidgetContents.setGeometry(
            0, 0, 380, 100 * listingCount
        )
        self.scrollAreaWidgetContents.update()
        self.scrollArea.update()

    def initIsNotLoggedInWidgets(self):
        self.not_logged_in_label = QLabel(None, self)
        self.not_logged_in_label.setGeometry(QRect(20, 20, 161, 16))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.not_logged_in_label.setFont(font)

        self.not_logged_in_label_2 = QLabel(None, self)
        self.not_logged_in_label_2.setGeometry(QRect(20, 40, 161, 49))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setWeight(50)
        font1.setKerning(True)
        self.not_logged_in_label_2.setFont(font1)
        self.not_logged_in_label_2.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )
        self.not_logged_in_label_2.setWordWrap(True)

        self.loginButton = QPushButton(None, self)
        self.loginButton.setGeometry(QRect(70, 80, 111, 30))
        self.loginButton.clicked.connect(self.openLoginWindow)

    def retranslateUi(self):
        self.setWindowTitle(
            QCoreApplication.translate(
                'MainWindow', 'S4C Anki', None
            )
        )
        self.searchBox.setPlaceholderText(
            QCoreApplication.translate(
                'MainWindow', 'Search', None
            )
        )
        self.cardTypeGroup.setTitle(
            QCoreApplication.translate(
                'MainWindow', 'Card Type', None
            )
        )
        self.includeVideo.setText(
            QCoreApplication.translate(
                'MainWindow', 'Include Video', None
            )
        )
        self.includeAudio.setText(
            QCoreApplication.translate(
                'MainWindow', 'Include Audio', None
            )
        )
        self.textOnly.setText(
            QCoreApplication.translate(
                'MainWindow', 'Text Only', None
            )
        )
        self.not_logged_in_label.setText(
            QCoreApplication.translate(
                'MainWindow', 'You are not logged in...', None
            )
        )
        self.not_logged_in_label_2.setText(
            QCoreApplication.translate(
                'MainWindow',
                'You must log in to use video and audio in your cards', None
            )
        )
        self.loginButton.setText(
            QCoreApplication.translate(
                'MainWindow', 'Login', None
            )
        )
        self.logged_in_label.setText(
            QCoreApplication.translate(
                'S4CWindow', 'Hello, {}'.format(self.api.name), None
            )
        )
        self.logged_in_label_2.setText(
            QCoreApplication.translate(
                'S4CWindow', 'You are logged in', None
            )
        )
        self.logoutButton.setText(
            QCoreApplication.translate(
                'S4CWindow', 'Log out', None
            )
        )
        self.loading.setText(
            QCoreApplication.translate(
                'S4CWindow', 'Loading...', None
            )
        )

    def updateLoginSpecificWidgets(self):
        if (self.api.token != ''):
            self.logged_in_label.setHidden(False)
            self.logged_in_label_2.setHidden(False)
            self.logoutButton.setHidden(False)
            self.not_logged_in_label.setHidden(True)
            self.not_logged_in_label_2.setHidden(True)
            self.cardTypeGroup.hide()
            self.loginButton.setHidden(True)
            self.includeVideo.setEnabled(True)
            self.includeAudio.setEnabled(True)
            self.cardTypeGroup.show()
        else:
            self.logged_in_label.setHidden(True)
            self.logged_in_label_2.setHidden(True)
            self.logoutButton.setHidden(True)
            self.not_logged_in_label.setHidden(False)
            self.not_logged_in_label_2.setHidden(False)
            self.loginButton.setHidden(False)
            self.cardTypeGroup.hide()
            self.textOnly.setChecked(True)
            self.includeVideo.setEnabled(False)
            self.includeAudio.setEnabled(False)
            self.cardTypeGroup.show()

    def openLoginWindow(self):
        self.loginWindow = LoginWindow(self)
        self.loginWindow.show()

    def logout(self):
        self.api.token = ''
        self.updateLoginSpecificWidgets()
