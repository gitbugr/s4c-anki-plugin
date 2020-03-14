from aqt.qt import (
    QTimer
)


class Debounce():
    timer = QTimer()

    def debounce(self, func, wait):
        self.timer.timeout.connect(func)
        self.timer.setSingleShot(True)

        def startTimer():
            self.timer.start(wait)

        return startTimer
