import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from db_connector import Database

class LibraryApp(tk.Tk):
    def __init__(root):
        super().__init__()
        root.title("Library Management Portal")
        root.geometry("1000x600")

        root.db = Database()

        root.style = ttk.Style()
        root.style.configure('Treeview', rowheight=25)
        root.style.configure('TButton', padding=5)

        root.notebook = ttk.Notebook(root)
        root.notebook.pack(pady=10, padx=10, fill='both', expand=True)

        root.add_tabs()

    def add_tabs(root):
        book_frame = ttk.Frame(root.notebook)
        root.notebook.add(book_frame, text = "Book Management")

        customer_frame = ttk.Frame(root.notebook)
        root.notebook.add(customer_frame, text = "Customer Management")

        transaction_frame = ttk.Frame(root.notebook)
        root.notebook.add(transaction_frame, text = "Transactions")

        root.setup_book_tab(book_frame)
        root.setup_customer_tab(customer_frame)
        root.setup_transaction_tab(transaction_frame)

    def setup_book_tab(root, frame):
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(tree_frame)
        scroll_y.pack(side='right', fill='y')

        cols = ("ID", "Title", "Author First Name", "Author Last Name", "Genre", "Publication Year", "Total Copies", "Available Copies")
        root.book_tree = ttk.Treeview(
            tree_frame,
            columns=cols,
            show='headings',
            yscrollcommand=scroll_y.set,
            selectmode='browse'
        )
        scroll_y.config(command=root.book_tree.yview)
        col_widths = [50, 250, 120, 120, 120, 60, 60, 80]
        for col, width in zip(cols, col_widths):
            root.book_tree.heading(col, text=col)
            root.book_tree.column(col, width=width, anchor='center')

        root.book_tree.pack(fill='both', expand=True)

        btn = ttk.Frame(frame)
        btn.pack(pady=10)

        ttk.Button(btn, text="Add Book", command=root.add_book).pack(side='left', padx=5)
        ttk.Button(btn, text="Edit Book", command=root.edit_book).pack(side='left', padx=5)
        ttk.Button(btn, text="Delete Book", command=root.delete_book).pack(side='left', padx=5)
        ttk.Button(btn, text="Refresh", command=root.load_books).pack(side='left', padx=5)

        root.load_books()

    def load_books(root):
        try:
            root.book_tree.delete(*root.book_tree.get_children())

            books = root.db.execute_query("""
                SELECT book_id, title, author_first_name, author_last_name, genre, publication_year, total_copies, available_copies
                FROM Book_Inventory
                ORDER BY title
            """).fetchall()

            for book in books:
                root.book_tree.insert('', 'end', values=book)

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load books:\n{str(e)}")

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
