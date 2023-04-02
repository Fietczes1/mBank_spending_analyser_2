from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QProgressBar, QPushButton

class SenderWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # create a layout for the window
        layout = QVBoxLayout()

        # create a progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)

        # create a button to increment the progress bar
        self.button = QPushButton("Increment", self)
        self.button.clicked.connect(self.increment_progress_bar)

        # add the progress bar and button to the layout
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.button)

        # create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def increment_progress_bar(self):
        self.progress_bar.setValue(self.progress_bar.value() + 10)

class ReceiverWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # create a layout for the window
        layout = QVBoxLayout()

        # create a progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)

        # add the progress bar to the layout
        layout.addWidget(self.progress_bar)

        # create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

class ProgressBarCommunicator(QObject):
    progress_bar_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def send_update_signal(self, some_list):
        self.progress_bar_updated.emit(some_list)

if __name__ == '__main__':
    # create the application
    app = QApplication([])

    # create the sender window and show it
    sender_window = SenderWindow()
    sender_window.show()

    # create the receiver window and show it
    receiver_window = ReceiverWindow()
    receiver_window.show()

    # create a progress bar communicator
    progress_bar_communicator = ProgressBarCommunicator()

    # connect the sender window to the communicator
    sender_window.progress_bar.valueChanged.connect(progress_bar_communicator.send_update_signal)

    # connect the communicator to the receiver window
    progress_bar_communicator.progress_bar_updated.connect(receiver_window.update_progress_bar)

    # run the application
    app.exec_()