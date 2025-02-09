import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from auth import authenticate
from admin import AdminWindow
from user import UserWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('ui/main_window.ui', self)
        self.loginButton.clicked.connect(self.login)
        self.changeLogoButton.clicked.connect(self.change_logo)
        self.set_logo()

    def set_logo(self):
        pixmap = QPixmap('logo.png')
        if not pixmap.isNull():
            self.logoLabel.setPixmap(pixmap.scaled(200, 200))
        else:
            print("Failed to load logo.png")

    def change_logo(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Logo", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        if file_path:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.logoLabel.setPixmap(pixmap.scaled(200, 200))
                pixmap.save('logo.png')
            else:
                print("Failed to load selected image")

    def login(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        role = authenticate(username, password)
        if role == 'admin':
            self.admin_window = AdminWindow(self)
            self.admin_window.show()
            self.hide()
        elif role == 'user':
            self.user_window = UserWindow(username, self)
            self.user_window.show()
            self.hide()
        else:
            QMessageBox.critical(self, "Error", "Invalid credentials")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())