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
        return False, "Username not found"
    if users[username]["password"] != hash_password(password):
        return False, "Wrong password"
    return True, "Login succeed!"


def delete_user(username: str) -> tuple[bool, str]:
    users = load_users()
    if username not in users:
        return False, "User not found"
    del users[username]
    save_users(users)
    return True, "User has been delete"


def update_user(old_username: str, new_username: str, email: str, new_password: str = "") -> tuple[bool, str]:
    users = load_users()
    if old_username not in users:
        return False, "User not found"
    if new_username != old_username and new_username in users:
        return False, "Username has been used by other"
    for uname, data in users.items():
        if uname != old_username and data.get("email", "").lower() == email.lower():
            return False, "Email has been used by other"
    record = users.pop(old_username)
    record["email"] = email
    if new_password:
        record["password"] = hash_password(new_password)
    users[new_username] = record
    save_users(users)
    return True, "User update successfully"


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
    books.append({"id": new_id, "title": judul, "writer": penulis, "year": tahun, "stock": stok})
    save_books(books)
    return True, "Book successfully added"


def update_book(book_id: int, judul: str, penulis: str, tahun: str, stok: int) -> tuple[bool, str]:
    books = load_books()
    for b in books:
        if int(b.get("id", 0)) == int(book_id):
            b["title"] = judul
            b["writer"] = penulis
            b["year"] = tahun
            b["stock"] = stok
            save_books(books)
            return True, "Book successfully added"
    return False, "Book hasn't found"


def delete_book(book_id: int) -> tuple[bool, str]:
    books = load_books()
    borrowings = load_borrowings()
    for p in borrowings:
        if int(p.get("book_id", 0)) == int(book_id) and p.get("status") == "Borrowed":
            return False, "Someone still borrowed the book"
    filtered = [b for b in books if int(b.get("id", 0)) != int(book_id)]
    if len(filtered) == len(books):
        return False, "Book hasn't found"
    save_books(filtered)
    return True, "Book successfully delete"


def find_book(book_id: int):
    for b in load_books():
        if int(b.get("id", 0)) == int(book_id):
            return b
    return None


def adjust_book_stock(book_id: int, delta: int) -> bool:
    books = load_books()
    for b in books:
        if int(b.get("id", 0)) == int(book_id):
            b["stock"] = int(b.get("stock", 0)) + delta
            if b["stock"] < 0:
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
        return False, "Username unfound"
    book = find_book(book_id)
    if book is None:
        return False, "Book hasn't found"
    if int(book.get("stock", 0)) <= 0:
        return False, "The book stock 0"
    borrowings = load_borrowings()
    new_id = get_next_borrowing_id(borrowings)
    borrowings.append({
        "id": new_id,
        "username": username,
        "book_id": int(book_id),
        "title": book.get("title", ""),
        "date": tanggal_pinjam,
        "duedate": tanggal_kembali,
        "status": "Borrowed",
    })
    save_borrowings(borrowings)
    adjust_book_stock(book_id, -1)
    return True, "Borrowing has been added"


def update_borrowing(borrow_id: int, username: str, book_id: int, tanggal_pinjam: str, tanggal_kembali: str, status: str) -> tuple[bool, str]:
    borrowings = load_borrowings()
    target = None
    for p in borrowings:
        if int(p.get("id", 0)) == int(borrow_id):
            target = p
            break
    if target is None:
        return False, "Borrowed data hasn't found"
    old_status = target.get("status")
    old_book_id = int(target.get("book_id", 0))
    new_book_id = int(book_id)
    if old_status == "Borrowed" and status == "Back" and old_book_id == new_book_id:
        adjust_book_stock(old_book_id, 1)
    elif old_status == "Back" and status == "Borrowed":
        book = find_book(new_book_id)
        if book is None:
            return False, "Book hasn't found"
        if int(book.get("stok", 0)) <= 0:
            return False, "The book stock 0"
        adjust_book_stock(new_book_id, -1)
    elif old_book_id != new_book_id and old_status == "Borrowed" and status == "Borrowed":
        book = find_book(new_book_id)
        if book is None:
            return False, "Book hasn't found"
        if int(book.get("stok", 0)) <= 0:
            return False, "The book stock 0"
        adjust_book_stock(old_book_id, 1)
        adjust_book_stock(new_book_id, -1)
    target["username"] = username
    target["book_id"] = new_book_id
    book_now = find_book(new_book_id)
    if book_now is not None:
        target["title"] = book_now.get("title", target.get("title", ""))
    target["date"] = tanggal_pinjam
    target["duedate"] = tanggal_kembali
    target["status"] = status
    save_borrowings(borrowings)
    return True, "Borrowed data updated successfully"


def delete_borrowing(borrow_id: int) -> tuple[bool, str]:
    borrowings = load_borrowings()
    target = None
    for p in borrowings:
        if int(p.get("id", 0)) == int(borrow_id):
            target = p
            break
    if target is None:
        return False, "Borrowed data hasn't found"
    if target.get("status") == "Borrowed":
        adjust_book_stock(int(target.get("book_id", 0)), 1)
    filtered = [p for p in borrowings if int(p.get("id", 0)) != int(borrow_id)]
    save_borrowings(filtered)
    return True, "Borrowed data has been delete."


class HoverButton(tk.Button):
    def __init__(self, master, bg_normal, bg_hover, **kwargs):
        super().__init__(master, bg=bg_normal, activebackground=bg_hover, **kwargs)
        self.bg_normal = bg_normal
        self.bg_hover = bg_hover
        self.bind("<Enter>", lambda e: self.config(bg=self.bg_hover))
        self.bind("<Leave>", lambda e: self.config(bg=self.bg_normal))