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
        #root.setup_customer_tab(customer_frame)
        #root.setup_transaction_tab(transaction_frame)

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
                ORDER BY book_id
            """).fetchall()

            for book in books:
                root.book_tree.insert('', 'end', values=book)

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load books:\n{str(e)}")

    def add_book(root, book_data=None):
        dialog = tk.Toplevel(root)
        dialog.title("Add New Book" if not book_data else "Edit Book")
        dialog.resizable(False, False)

        fields = [
            ("Title:", "title"),
            ("Author First Name:", "author_first_name"),
            ("Author Last Name:", "author_last_name"),
            ("Genre:", "genre"),
            ("Publication Year:", "publication_year"),
            ("Total Copies:", "total_copies"),
            ("Available Copies:", "available_copies")
        ]

        entries = {}
        for row, (label, name) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=row, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(dialog)
            entry.grid(row=row, column=1, padx=5, pady=5)

            if book_data:
                entry.insert(0, book_data[row+1])
            entries[name] = entry

        submit_text = "Add Book" if not book_data else "Update"
        ttk.Button(
            dialog,
            text=submit_text,
            command=lambda: root.save_book(
                entries,
                dialog,
                book_data[0] if book_data else None
            )
        ).grid(row=len(fields), columnspan=2, pady=10)

    def save_book(root, entries, dialog, book_id=None):
        try:
            total_copies = int(entries['total_copies'].get())
            available_copies = int(entries['available_copies'].get())

            if available_copies > total_copies:
                raise ValueError("Available copies cannot exceed total copies")
            
            data = (
                entries['title'].get(),
                entries['author_first_name'].get(),
                entries['author_last_name'].get(),
                entries['genre'].get(),
                entries['publication_year'].get(),
                total_copies,
                available_copies
            )

            if book_id:
                root.db.execute_query("""
                    UPDATE Book_Inventory 
                    SET title=?, author_first_name=?, author_last_name=?, genre=?, publication_year=?, total_copies=?, available_copies=?
                    WHERE book_id=?
                """, (*data, book_id))
            else:
                root.db.execute_query("""
                    INSERT INTO Book_Inventory (title, author_first_name, author_last_name, genre, publication_year, total_copies, available_copies)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, data)

                root.db.conn.commit()
                root.load_books()
                dialog.destroy()
                messagebox.showinfo("Success", "Book saved successfully")
        
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Database Error", f"Operation failed: {str(e)}")

    def edit_book(root):
        selected = root.book_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to delete")
            return
        
        book_data = root.book_tree.item(selected, 'values')
        root.add_book(book_data)

    def delete_book(root):
        selected = root.book_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to delete")
            return

        book_id = root.book_tree.item(selected, 'values')[0]
        if messagebox.askyesno("Confirm", "Delete this book permanently?"):
            try:
                root.db.execute_query("DELETE FROM Book_Inventory WHERE book_id=?",(book_id,))
                root.db.conn.commit()
                root.load_books()
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete book:\n{str(e)}")

    def setup_member_tab(root, frame):
        label = ttk.Label(frame, text = "Member Management", font = ('Arial', 12))
        label.pack(pady=50) 


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
