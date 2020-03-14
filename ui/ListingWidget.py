import urllib.request
from aqt.qt import (
    Qt,
    QRect,
    QFont,
    QLabel,
    QThread,
    QImage,
    QPixmap,
    QWidget,
    pyqtSignal,
    QPushButton,
    QCoreApplication
)


class ListingWidget(QWidget):

    def __init__(self, parent, programmeDetails, mainWindow):
        super().__init__(parent)
        self.programmeDetails = programmeDetails
        self.mainWindow = mainWindow
        self.initUi()

    def initUi(self):
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.title = QLabel(self)
        self.title.setGeometry(QRect(90, 10, 121, 16))
        self.title.setFont(font)
        self.date = QLabel(self)
        self.date.setGeometry(QRect(240, 10, 121, 16))
        self.date.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter
        )
        self.thumbnail = QLabel(self)
        self.thumbnail.setGeometry(QRect(0, 10, 81, 81))
        self.thumbnail.setTextFormat(Qt.RichText)
        self.thumbnail.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )

        url = 'https://s4c.cymru/amg/landscape/80x80/{}'.format(
            self.programmeDetails['thumbnail_url']
        )
        self.downloadThread = DownloadThread(url)
        self.downloadThread.start()
        self.downloadThread.dataDownloaded.connect(self.updateThumbnail)

        self.description = QLabel(self)
        self.description.setGeometry(QRect(90, 30, 261, 41))
        self.description.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )
        self.description.setWordWrap(True)
        self.runtime = QLabel(self)
        self.runtime.setGeometry(QRect(90, 70, 131, 16))
        self.runtime.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )
        self.runtime.setWordWrap(True)
        self.generate = QPushButton(self)
        self.generate.setGeometry(QRect(271, 60, 91, 32))

        self.retranslateUi()
        self.show()

    def retranslateUi(self):
        self.description.setText(
            QCoreApplication.translate(
                'ListingWidget',
                (self.programmeDetails['short_billing'] or '')[:70] + '...',
                None
            )
        )
        self.runtime.setText(
            str(self.programmeDetails['duration']) +
            QCoreApplication.translate(
                'ListingWidget',
                'mins',
                None
            )
        )
        self.generate.setText(
            QCoreApplication.translate(
                'ListingWidget',
                'Generate',
                None
            )
        )
        self.title.setText(
            QCoreApplication.translate(
                'ListingWidget',
                self.programmeDetails['title'].strip(),
                None
            )
        )
        self.date.setText(
            QCoreApplication.translate(
                'ListingWidget',
                self.programmeDetails['clic_aired'],
                None
            )
        )

    def updateThumbnail(self):
        image = QImage()
        image.loadFromData(self.downloadThread.getData())
        self.thumbnail.setPixmap(QPixmap(image))
        self.update()
        self.mainWindow.loading.hide()


class DownloadThread(QThread):
    dataDownloaded = pyqtSignal()

    def __init__(self, url):
        QThread.__init__(self)
        self.url = url
        self._data = None

    def run(self):
        self._data = urllib.request.urlopen(self.url).read()
        self.dataDownloaded.emit()

    def getData(self):
        return self._data
