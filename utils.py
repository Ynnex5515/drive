import os
import json
import fitz  # PyMuPDF

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def list_pdfs(folder):
    return [f for f in os.listdir(folder) if allowed_file(f)]

def search_pdfs(query, folder):
    return [f for f in list_pdfs(folder) if query.lower() in f.lower()]

def load_favorites(username):
    with open('favorites.json', 'r') as f:
        favorites = json.load(f)
    return favorites.get(username, [])

def save_favorites(username, favorites):
    with open('favorites.json', 'r') as f:
        all_favorites = json.load(f)
    all_favorites[username] = favorites
    with open('favorites.json', 'w') as f:
        json.dump(all_favorites, f)

def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

def secure_pdf(file_path):
    doc = fitz.open(file_path)
    permissions = fitz.PDF_PERM_ACCESSIBILITY | fitz.PDF_PERM_COPY | fitz.PDF_PERM_ANNOTATE
    doc.save(file_path, permissions=permissions)