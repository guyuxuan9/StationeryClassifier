import sys
import cv2
import datetime
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QListWidget, QTextEdit


class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        # Create the camera object
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, 640)  # Set width of camera view
        self.camera.set(4, 480)  # Set height of camera view

        # Create the UI elements
        self.camera_view = QLabel()
        self.prompt_label = QLabel()
        self.image_name_label = QLabel()
        self.time_label = QLabel()
        self.interval_input = QLineEdit()
        self.set_interval_button = QPushButton("Set Interval(s)")
        self.take_picture_button = QPushButton("Take Picture")
        self.auto_detect_button = QPushButton("Auto vs. Manual")
        self.auto_detect_status_label = QLabel("Manual")
        self.console_label = QLabel("Console:")
        self.console_text_edit = QTextEdit()

        # Set up the layout
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        middle_layout = QVBoxLayout()
        bottom_layout = QHBoxLayout()

        top_layout.addWidget(self.camera_view)
        
        middle_layout.addWidget(self.time_label)
        middle_layout.addWidget(self.interval_input)
        middle_layout.addWidget(self.set_interval_button)
        middle_layout.addWidget(self.take_picture_button)
        middle_layout.addWidget(self.auto_detect_button)
        middle_layout.addWidget(self.auto_detect_status_label)

        bottom_layout.addWidget(self.console_label)
        bottom_layout.addWidget(self.console_text_edit)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        # Connect button signals
        self.set_interval_button.clicked.connect(self.set_interval)
        self.take_picture_button.clicked.connect(self.take_picture)
        self.auto_detect_button.clicked.connect(self.toggle_auto_detect)

        self.interval = 1  # Default interval in seconds
        self.auto_detect = False  # AutoDetect state, initially disabled
        self.last_picture_time = datetime.datetime.now()  # Initialize last picture time

        self.update_auto_detect_status()

        # Set up the timer for camera updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_camera)
        self.timer.start(30)  # Update every 30 milliseconds (33 fps)

    def update_camera(self):
        ret, frame = self.camera.read()

        # Convert the frame to QImage
        if ret:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, _ = image.shape
            q_image = QImage(image.data, width, height, QImage.Format_RGB888)
            self.camera_view.setPixmap(QPixmap.fromImage(q_image))
            self.camera_view.setScaledContents(True)

            # Check if the elapsed time since the last picture exceeds the interval
            current_time = datetime.datetime.now()
            elapsed_time = (current_time - self.last_picture_time).total_seconds()
            if self.auto_detect and elapsed_time >= self.interval:
                self.take_picture()
                self.last_picture_time = current_time

    def set_interval(self):
        interval_text = self.interval_input.text()
        try:
            self.interval = float(interval_text)
            self.print_to_console("Interval set: {}".format(self.interval))
        except ValueError:
            self.print_to_console("Invalid interval input.")

    def take_picture(self):
        ret, frame = self.camera.read()

        if ret:
            # Save the image
            image_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
            cv2.imwrite(image_name, frame)
            self.print_to_console("Image saved: {}".format(image_name))
            self.prompt_label.setText("Picture saved.")
            self.image_name_label.setText(image_name)

    def toggle_auto_detect(self):
        self.auto_detect = not self.auto_detect
        self.update_auto_detect_status()

    def update_auto_detect_status(self):
        if self.auto_detect:
            self.auto_detect_status_label.setText("Auto")
        else:
            self.auto_detect_status_label.setText("Manual")

    def closeEvent(self, event):
        # Release the camera when the UI is closed
        self.camera.release()
        event.accept()

    def print_to_console(self, message):
        print(message)  # Print to the terminal
        self.console_text_edit.append(message)  # Append the message to the text edit

        # Scroll to the bottom of the text edit to show the latest message
        self.console_text_edit.verticalScrollBar().setValue(self.console_text_edit.verticalScrollBar().maximum())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = CameraApp()
    window.setWindowTitle("Camera App")
    window.show()

    sys.exit(app.exec_())
