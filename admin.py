import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTreeWidgetItem
from PyQt5.uic import loadUi
from utils import UPLOAD_FOLDER, allowed_file, list_pdfs, search_pdfs, secure_pdf
from auth import add_user, update_admin_credentials

class AdminWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        loadUi('ui/admin_window.ui', self)
        self.uploadButton.clicked.connect(self.upload_pdf)
        self.createFolderButton.clicked.connect(self.create_folder)
        self.addUserButton.clicked.connect(self.add_user)
        self.updateCredentialsButton.clicked.connect(self.update_credentials)
        self.logoutButton.clicked.connect(self.logout)
        self.refresh_file_tree()

    def upload_pdf(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload PDF", "", "PDF Files (*.pdf)", options=options)
        if file_path and allowed_file(file_path):
            current_item = self.fileTree.currentItem()
            folder = current_item.text(0) if current_item else UPLOAD_FOLDER
            filename = os.path.basename(file_path)
            dest_path = os.path.join(folder, filename)
            os.makedirs(folder, exist_ok=True)
            os.rename(file_path, dest_path)
            secure_pdf(dest_path)
            self.refresh_file_tree()
        else:
            QMessageBox.critical(self, "Error", "Invalid file type")

    def create_folder(self):
        current_item = self.fileTree.currentItem()
        parent_folder = current_item.text(0) if current_item else UPLOAD_FOLDER
        folder_name, ok = QFileDialog.getSaveFileName(self, "Create Folder", parent_folder)
        if ok:
            os.makedirs(folder_name, exist_ok=True)
            self.refresh_file_tree()

    def refresh_file_tree(self):
        self.fileTree.clear()
        self.add_items(self.fileTree.invisibleRootItem(), UPLOAD_FOLDER)

    def add_items(self, parent, path):
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            tree_item = QTreeWidgetItem(parent, [item])
            if os.path.isdir(full_path):
                self.add_items(tree_item, full_path)

    def add_user(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        if add_user(username, password, 'user'):
            QMessageBox.information(self, "Success", "User added successfully")
        else:
            QMessageBox.critical(self, "Error", "User already exists")

    def update_credentials(self):
        new_username = self.newUsernameInput.text()
        new_password = self.newPasswordInput.text()
        if update_admin_credentials(new_username, new_password):
            QMessageBox.information(self, "Success", "Admin credentials updated successfully")
        else:
            QMessageBox.critical(self, "Error", "Failed to update admin credentials")

    def logout(self):
        self.main_window.show()
        self.close()