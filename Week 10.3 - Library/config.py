import tkinter as tk
import json
import os
import hashlib


APP_WIDTH = 1280
APP_HEIGHT = 720

USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")
BOOKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books.json")
BORROWINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "borrowings.json")


COLOR_PRIMARY = "#AEAC78"
COLOR_ACCENT = "#4C4541"
COLOR_ACCENT_DARK = "#4C4541"
COLOR_BG = "#FCF0DA"
COLOR_CARD = "#ffffff"
COLOR_TEXT = "#4C4541"
COLOR_MUTED = "#4C4541"
COLOR_SUCCESS = "#5C7057"
COLOR_DANGER = "#A14646"


FONT_TITLE = ("Linux Libertine G", 26, "bold")
FONT_SUBTITLE = ("Linux Libertine G", 12)
FONT_NAV = ("Linux Libertine G", 11, "bold")
FONT_CARD_TITLE = ("Linux Libertine G", 14, "bold")
FONT_CARD_BODY = ("Linux Libertine G", 10)
FONT_LABEL = ("Linux Libertine G", 11)
FONT_BUTTON = ("Linux Libertine G", 11, "bold")


ARTIKEL_PERPUSTAKAAN = [
    {
        "judul": "BOOK RECOMENDATION FOR THIS WEEK",
        "ringkasan": "This week filled with fantasy, biograph, and more"
                     "you can explore many types of book",
        "kategori": "Recommendation",
    },
    {
        "judul": "EASY WAY TO READ NOVEL",
        "ringkasan": "Create a small target every week to read"
                     "novel and don't fotget to write things"
                     "things you've get through novel",
        "kategori": "Tips & Trick",
    },
]


DEFAULT_BOOKS = [
    {"id": 1, "title": "The Song of Achilles", "writer": "Madeline Miller", "year": "2011", "stock": 5},
    {"id": 2, "title": "Project Hail Mary", "writer": "Andy Weir", "year": "2021", "stock": 3},
    {"id": 3, "title": "Educated", "writer": "Tara Westover", "year": "2018", "stock": 4},
]


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_users() -> dict:
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_users(users: dict) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def register_user(username: str, email: str, password: str) -> tuple[bool, str]:
    users = load_users()
    if username in users:
        return False, "Username sudah terdaftar. Silakan gunakan username lain."
    for data in users.values():
        if data.get("email", "").lower() == email.lower():
            return False, "Email sudah terdaftar. Silakan gunakan email lain."
    users[username] = {
        "email": email,
        "password": hash_password(password),
    }
    save_users(users)
    return True, "Signup succeed, please login!"


def verify_login(username: str, password: str) -> tuple[bool, str]:
    users = load_users()
    if username not in users:
        return False, "Username tidak ditemukan."
    if users[username]["password"] != hash_password(password):
        return False, "Password salah."
    return True, "Login berhasil!"


def delete_user(username: str) -> tuple[bool, str]:
    users = load_users()
    if username not in users:
        return False, "User tidak ditemukan."
    del users[username]
    save_users(users)
    return True, "User berhasil dihapus."


def update_user(old_username: str, new_username: str, email: str, new_password: str = "") -> tuple[bool, str]:
    users = load_users()
    if old_username not in users:
        return False, "User tidak ditemukan."
    if new_username != old_username and new_username in users:
        return False, "Username baru sudah dipakai user lain."
    for uname, data in users.items():
        if uname != old_username and data.get("email", "").lower() == email.lower():
            return False, "Email sudah dipakai user lain."
    record = users.pop(old_username)
    record["email"] = email
    if new_password:
        record["password"] = hash_password(new_password)
    users[new_username] = record
    save_users(users)
    return True, "User berhasil diperbarui."


def load_books() -> list:
    if not os.path.exists(BOOKS_FILE):
        save_books(DEFAULT_BOOKS)
        return list(DEFAULT_BOOKS)
    try:
        with open(BOOKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []


def save_books(books: list) -> None:
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)


def get_next_book_id(books: list) -> int:
    if not books:
        return 1
    return max(int(b.get("id", 0)) for b in books) + 1


def add_book(judul: str, penulis: str, tahun: str, stok: int) -> tuple[bool, str]:
    books = load_books()
    new_id = get_next_book_id(books)
    books.append({"id": new_id, "judul": judul, "penulis": penulis, "tahun": tahun, "stok": stok})
    save_books(books)
    return True, "Buku berhasil ditambahkan."


def update_book(book_id: int, judul: str, penulis: str, tahun: str, stok: int) -> tuple[bool, str]:
    books = load_books()
    for b in books:
        if int(b.get("id", 0)) == int(book_id):
            b["judul"] = judul
            b["penulis"] = penulis
            b["tahun"] = tahun
            b["stok"] = stok
            save_books(books)
            return True, "Buku berhasil diperbarui."
    return False, "Buku tidak ditemukan."


def delete_book(book_id: int) -> tuple[bool, str]:
    books = load_books()
    borrowings = load_borrowings()
    for p in borrowings:
        if int(p.get("book_id", 0)) == int(book_id) and p.get("status") == "Dipinjam":
            return False, "Buku tidak bisa dihapus karena sedang dipinjam."
    filtered = [b for b in books if int(b.get("id", 0)) != int(book_id)]
    if len(filtered) == len(books):
        return False, "Buku tidak ditemukan."
    save_books(filtered)
    return True, "Buku berhasil dihapus."


def find_book(book_id: int):
    for b in load_books():
        if int(b.get("id", 0)) == int(book_id):
            return b
    return None


def adjust_book_stock(book_id: int, delta: int) -> bool:
    books = load_books()
    for b in books:
        if int(b.get("id", 0)) == int(book_id):
            b["stok"] = int(b.get("stok", 0)) + delta
            if b["stok"] < 0:
                return False
            save_books(books)
            return True
    return False


def load_borrowings() -> list:
    if not os.path.exists(BORROWINGS_FILE):
        return []
    try:
        with open(BORROWINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []


def save_borrowings(borrowings: list) -> None:
    with open(BORROWINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(borrowings, f, indent=2, ensure_ascii=False)


def get_next_borrowing_id(borrowings: list) -> int:
    if not borrowings:
        return 1
    return max(int(p.get("id", 0)) for p in borrowings) + 1


def add_borrowing(username: str, book_id: int, tanggal_pinjam: str, tanggal_kembali: str) -> tuple[bool, str]:
    users = load_users()
    if username not in users:
        return False, "Username tidak terdaftar."
    book = find_book(book_id)
    if book is None:
        return False, "Buku tidak ditemukan."
    if int(book.get("stok", 0)) <= 0:
        return False, "Stok buku habis."
    borrowings = load_borrowings()
    new_id = get_next_borrowing_id(borrowings)
    borrowings.append({
        "id": new_id,
        "username": username,
        "book_id": int(book_id),
        "judul": book.get("judul", ""),
        "tanggal_pinjam": tanggal_pinjam,
        "tanggal_kembali": tanggal_kembali,
        "status": "Dipinjam",
    })
    save_borrowings(borrowings)
    adjust_book_stock(book_id, -1)
    return True, "Peminjaman berhasil ditambahkan."


def update_borrowing(borrow_id: int, username: str, book_id: int, tanggal_pinjam: str, tanggal_kembali: str, status: str) -> tuple[bool, str]:
    borrowings = load_borrowings()
    target = None
    for p in borrowings:
        if int(p.get("id", 0)) == int(borrow_id):
            target = p
            break
    if target is None:
        return False, "Data peminjaman tidak ditemukan."
    old_status = target.get("status")
    old_book_id = int(target.get("book_id", 0))
    new_book_id = int(book_id)
    if old_status == "Dipinjam" and status == "Kembali" and old_book_id == new_book_id:
        adjust_book_stock(old_book_id, 1)
    elif old_status == "Kembali" and status == "Dipinjam":
        book = find_book(new_book_id)
        if book is None:
            return False, "Buku tidak ditemukan."
        if int(book.get("stok", 0)) <= 0:
            return False, "Stok buku habis."
        adjust_book_stock(new_book_id, -1)
    elif old_book_id != new_book_id and old_status == "Dipinjam" and status == "Dipinjam":
        book = find_book(new_book_id)
        if book is None:
            return False, "Buku tidak ditemukan."
        if int(book.get("stok", 0)) <= 0:
            return False, "Stok buku habis."
        adjust_book_stock(old_book_id, 1)
        adjust_book_stock(new_book_id, -1)
    target["username"] = username
    target["book_id"] = new_book_id
    book_now = find_book(new_book_id)
    if book_now is not None:
        target["judul"] = book_now.get("judul", target.get("judul", ""))
    target["tanggal_pinjam"] = tanggal_pinjam
    target["tanggal_kembali"] = tanggal_kembali
    target["status"] = status
    save_borrowings(borrowings)
    return True, "Data peminjaman berhasil diperbarui."


def delete_borrowing(borrow_id: int) -> tuple[bool, str]:
    borrowings = load_borrowings()
    target = None
    for p in borrowings:
        if int(p.get("id", 0)) == int(borrow_id):
            target = p
            break
    if target is None:
        return False, "Data peminjaman tidak ditemukan."
    if target.get("status") == "Dipinjam":
        adjust_book_stock(int(target.get("book_id", 0)), 1)
    filtered = [p for p in borrowings if int(p.get("id", 0)) != int(borrow_id)]
    save_borrowings(filtered)
    return True, "Data peminjaman berhasil dihapus."


class HoverButton(tk.Button):
    def __init__(self, master, bg_normal, bg_hover, **kwargs):
        super().__init__(master, bg=bg_normal, activebackground=bg_hover, **kwargs)
        self.bg_normal = bg_normal
        self.bg_hover = bg_hover
        self.bind("<Enter>", lambda e: self.config(bg=self.bg_hover))
        self.bind("<Leave>", lambda e: self.config(bg=self.bg_normal))