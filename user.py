from PyQt5.QtWidgets import QMainWindow, QListWidgetItem
from PyQt5.uic import loadUi
from utils import list_pdfs, search_pdfs, load_favorites, save_favorites

class UserWindow(QMainWindow):
    def __init__(self, username, main_window):
        super().__init__()
        self.username = username
        self.main_window = main_window
        loadUi('ui/user_window.ui', self)
        self.searchInput.textChanged.connect(self.search_pdfs)
        self.addToFavoritesButton.clicked.connect(self.add_to_favorites)
        self.removeFromFavoritesButton.clicked.connect(self.remove_from_favorites)
        self.logoutButton.clicked.connect(self.logout)
        self.refresh_file_list()
        self.refresh_favorites_list()

    def refresh_file_list(self):
        self.fileList.clear()
        for file_name in list_pdfs('uploads'):
            item = QListWidgetItem(file_name)
            self.fileList.addItem(item)

    def search_pdfs(self):
        query = self.searchInput.text()
        self.fileList.clear()
        for file_name in search_pdfs(query, 'uploads'):
            item = QListWidgetItem(file_name)
            self.fileList.addItem(item)

    def refresh_favorites_list(self):
        self.favoritesList.clear()
        favorites = load_favorites(self.username)
        for file_name in favorites:
            self.favoritesList.addItem(file_name)

    def add_to_favorites(self):
        selected_items = self.fileList.selectedItems()
        if selected_items:
            file_name = selected_items[0].text()
            favorites = load_favorites(self.username)
            if file_name not in favorites:
                favorites.append(file_name)
                save_favorites(self.username, favorites)
                self.refresh_favorites_list()

    def remove_from_favorites(self):
        selected_items = self.favoritesList.selectedItems()
        if selected_items:
            file_name = selected_items[0].text()
            favorites = load_favorites(self.username)
            if file_name in favorites:
                favorites.remove(file_name)
                save_favorites(self.username, favorites)
                self.refresh_favorites_list()

    def logout(self):
        self.main_window.show()
        self.close()