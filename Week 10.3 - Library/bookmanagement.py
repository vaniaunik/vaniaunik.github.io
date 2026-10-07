import tkinter as tk
from tkinter import ttk, messagebox
from config import (
    COLOR_PRIMARY, COLOR_ACCENT, COLOR_ACCENT_DARK, COLOR_BG, COLOR_CARD,
    COLOR_TEXT, COLOR_MUTED, COLOR_SUCCESS, COLOR_DANGER,
    FONT_NAV, FONT_LABEL, FONT_BUTTON, HoverButton,
    load_books, add_book, update_book, delete_book,
)


class BookManagementPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.selected_id = None

        navbar = tk.Frame(self, bg=COLOR_PRIMARY, height=60)
        navbar.pack(fill="x", side="top")
        navbar.pack_propagate(False)

        tk.Label(
            navbar, text="𝓥LIBRARY",
            bg=COLOR_PRIMARY, fg="white", font=("Linux Libertine G", 14, "bold")
        ).pack(side="left", padx=20)

        nav_left = tk.Frame(navbar, bg=COLOR_PRIMARY)
        nav_left.pack(side="left", padx=10)

        HoverButton(
            nav_left, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
            text="Booklist", fg="white", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2",
            command=lambda: controller.show_frame("BookManagementPage")
        ).pack(side="left", padx=4)

        HoverButton(
            nav_left, bg_normal=COLOR_PRIMARY, bg_hover="#4C4541",
            text="Borrow", fg="white", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2",
            command=lambda: controller.show_frame("BorrowingManagementPage")
        ).pack(side="left", padx=4)

        HoverButton(
            nav_left, bg_normal=COLOR_PRIMARY, bg_hover="#34495e",
            text="User", fg="white", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2",
            command=lambda: controller.show_frame("UsersManagementPage")
        ).pack(side="left", padx=4)

        HoverButton(
            nav_left, bg_normal=COLOR_PRIMARY, bg_hover="#34495e",
            text="Blog", fg="white", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2",
            command=lambda: controller.show_frame("HomePage")
        ).pack(side="left", padx=4)

        self.nav_right = tk.Frame(navbar, bg=COLOR_PRIMARY)
        self.nav_right.pack(side="right", padx=20)

        self.user_label = tk.Label(
            self.nav_right, text="", bg=COLOR_PRIMARY, fg="white", font=FONT_NAV
        )
        self.user_label.pack(side="left", padx=(0, 12))

        HoverButton(
            self.nav_right, bg_normal="#c0392b", bg_hover="#a93226",
            text="Logout", fg="white", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2", command=controller.logout
        ).pack(side="left")

        content = tk.Frame(self, bg=COLOR_BG)
        content.pack(fill="both", expand=True, padx=25, pady=18)

        tk.Label(
            content, text="Book Management",
            bg=COLOR_BG, fg=COLOR_TEXT, font=("Linux Libertine G", 18, "bold")
        ).pack(anchor="w", pady=(0, 12))

        body = tk.Frame(content, bg=COLOR_BG)
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=0)
        body.grid_columnconfigure(1, weight=1)

        form = tk.Frame(body, bg=COLOR_CARD, padx=22, pady=20,
                        highlightthickness=1, highlightbackground="#dfe6e9")
        form.grid(row=0, column=0, sticky="ns", padx=(0, 16))

        tk.Label(form, text="Book Form", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=("Linux Libertine G", 13, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        tk.Label(form, text="Title", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=1, column=0, columnspan=2, sticky="w")
        self.entry_judul = tk.Entry(form, font=FONT_LABEL, width=30, relief="solid", bd=1)
        self.entry_judul.grid(row=2, column=0, columnspan=2, pady=(4, 10), ipady=4)

        tk.Label(form, text="Writer", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=3, column=0, columnspan=2, sticky="w")
        self.entry_penulis = tk.Entry(form, font=FONT_LABEL, width=30, relief="solid", bd=1)
        self.entry_penulis.grid(row=4, column=0, columnspan=2, pady=(4, 10), ipady=4)

        tk.Label(form, text="Year", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=5, column=0, columnspan=2, sticky="w")
        self.entry_tahun = tk.Entry(form, font=FONT_LABEL, width=30, relief="solid", bd=1)
        self.entry_tahun.grid(row=6, column=0, columnspan=2, pady=(4, 10), ipady=4)

        tk.Label(form, text="Stock", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=7, column=0, columnspan=2, sticky="w")
        self.entry_stok = tk.Entry(form, font=FONT_LABEL, width=30, relief="solid", bd=1)
        self.entry_stok.grid(row=8, column=0, columnspan=2, pady=(4, 16), ipady=4)

        HoverButton(
            form, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
            text="Add", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.handle_add
        ).grid(row=9, column=0, sticky="ew", ipady=7, padx=(0, 5))

        HoverButton(
            form, bg_normal=COLOR_SUCCESS, bg_hover="#1e8449",
            text="Update", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.handle_update
        ).grid(row=9, column=1, sticky="ew", ipady=7, padx=(5, 0))

        HoverButton(
            form, bg_normal=COLOR_DANGER, bg_hover="#a93226",
            text="Delete", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.handle_delete
        ).grid(row=10, column=0, sticky="ew", ipady=7, pady=(8, 0), padx=(0, 5))

        HoverButton(
            form, bg_normal=COLOR_MUTED, bg_hover="#707b7c",
            text="Clear", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.clear_fields
        ).grid(row=10, column=1, sticky="ew", ipady=7, pady=(8, 0), padx=(5, 0))

        right = tk.Frame(body, bg=COLOR_CARD,
                         highlightthickness=1, highlightbackground="#dfe6e9")
        right.grid(row=0, column=1, sticky="nsew")
        body.grid_rowconfigure(0, weight=1)

        search_frame = tk.Frame(right, bg=COLOR_CARD)
        search_frame.pack(fill="x", padx=16, pady=(14, 8))

        tk.Label(search_frame, text="Search:", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).pack(side="left")
        self.entry_search = tk.Entry(search_frame, font=FONT_LABEL, width=28, relief="solid", bd=1)
        self.entry_search.pack(side="left", padx=(8, 8), ipady=3)
        self.entry_search.bind("<KeyRelease>", lambda e: self.refresh_table())

        columns = ("id", "title", "writer", "year", "stock")
        self.tree = ttk.Treeview(right, columns=columns, show="headings", height=18)
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("writer", text="Writer")
        self.tree.heading("year", text="Year")
        self.tree.heading("stock", text="Stock")
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("title", width=300)
        self.tree.column("writer", width=200)
        self.tree.column("year", width=80, anchor="center")
        self.tree.column("stock", width=70, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def on_show(self):
        if not self.controller.current_user:
            self.controller.show_frame("SignInPage")
            return
        self.user_label.config(text="".join(["\U0001F464 ", str(self.controller.current_user)]))
        self.clear_fields()
        self.entry_search.delete(0, tk.END)
        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        keyword = self.entry_search.get().strip().lower()
        for b in load_books():
            judul = str(b.get("title", ""))
            penulis = str(b.get("writer", ""))
            if keyword and keyword not in judul.lower() and keyword not in penulis.lower():
                continue
            self.tree.insert("", "end", values=(
                b.get("id", ""),
                b.get("title", ""),
                b.get("writer", ""),
                b.get("year", ""),
                b.get("stock", ""),
            ))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        if not values:
            return
        self.selected_id = values[0]
        self.entry_judul.delete(0, tk.END)
        self.entry_judul.insert(0, values[1])
        self.entry_penulis.delete(0, tk.END)
        self.entry_penulis.insert(0, values[2])
        self.entry_tahun.delete(0, tk.END)
        self.entry_tahun.insert(0, values[3])
        self.entry_stok.delete(0, tk.END)
        self.entry_stok.insert(0, values[4])

    def read_form(self):
        judul = self.entry_judul.get().strip()
        penulis = self.entry_penulis.get().strip()
        tahun = self.entry_tahun.get().strip()
        stok_text = self.entry_stok.get().strip()
        return judul, penulis, tahun, stok_text

    def handle_add(self):
        judul, penulis, tahun, stok_text = self.read_form()
        if not judul or not penulis or not tahun or not stok_text:
            messagebox.showwarning("Data incomplete", "Please fill all the book column")
            return
        try:
            stok = int(stok_text)
            if stok < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Stok invalid", "Stock should be numbered >= 0.")
            return
        success, message = add_book(judul, penulis, tahun, stok)
        if success:
            messagebox.showinfo("Succeed", message)
            self.clear_fields()
            self.refresh_table()
        else:
            messagebox.showerror("Failed", message)

    def handle_update(self):
        if self.selected_id is None:
            messagebox.showwarning("Wasn't choose", "Choose the book on the table first")
            return
        judul, penulis, tahun, stok_text = self.read_form()
        if not judul or not penulis or not tahun or not stok_text:
            messagebox.showwarning("Data incomplete", "Please fill all the book column")
            return
        try:
            stok = int(stok_text)
            if stok < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Stock invalid", "Stock should be numbered >= 0.")
            return
        success, message = update_book(self.selected_id, judul, penulis, tahun, stok)
        if success:
            messagebox.showinfo("Succeed", message)
            self.clear_fields()
            self.refresh_table()
        else:
            messagebox.showerror("Failed", message)

    def handle_delete(self):
        if self.selected_id is None:
            messagebox.showwarning("Wasn't choose", "Choose the book on the table first")
            return
        confirm = messagebox.askyesno("Confirm", "Sure you want to delete this book?")
        if not confirm:
            return
        success, message = delete_book(self.selected_id)
        if success:
            messagebox.showinfo("Succeed", message)
            self.clear_fields()
            self.refresh_table()
        else:
            messagebox.showerror("Failed", message)

    def clear_fields(self):
        self.selected_id = None
        self.entry_judul.delete(0, tk.END)
        self.entry_penulis.delete(0, tk.END)
        self.entry_tahun.delete(0, tk.END)
        self.entry_stok.delete(0, tk.END)
        selection = self.tree.selection()
        if selection:
            self.tree.selection_remove(selection)