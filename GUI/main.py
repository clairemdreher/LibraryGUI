import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from db_connector import Database
from datetime import datetime, timedelta

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

        checkedout_frame = ttk.Frame(root.notebook)
        root.notebook.add(checkedout_frame, text = "Checked Out Books")

        transaction_frame = ttk.Frame(root.notebook)
        root.notebook.add(transaction_frame, text = "Transactions")

        root.setup_book_tab(book_frame)
        root.setup_customer_tab(customer_frame)
        root.setup_checkedout_tab(checkedout_frame)
        root.setup_transaction_tab(transaction_frame)

    def setup_book_tab(root, frame):
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(tree_frame)
        scroll_y.pack(side='right', fill='y')

        cols = ("Book ID", "Title", "Author First Name", "Author Last Name", "Genre", "Year", "Total Copies", "Available Copies")
        root.book_tree = ttk.Treeview(
            tree_frame,
            columns=cols,
            show='headings',
            yscrollcommand=scroll_y.set,
            selectmode='browse'
        )
        scroll_y.config(command=root.book_tree.yview)
        col_widths = [50, 200, 120, 120, 120, 60, 60, 80]
        for col, width in zip(cols, col_widths):
            root.book_tree.heading(col, text=col)
            root.book_tree.column(col, width=width, anchor='center')

        root.book_tree.pack(fill='both', expand=True)

        btn = ttk.Frame(frame)
        btn.pack(pady=10)

        search_frame = ttk.Frame(frame)
        search_frame.pack(pady=5, padx=10, fill='x')

        ttk.Label(search_frame, text="Search Author:").pack(side='left', padx=5)
        root.author_search_entry = ttk.Entry(search_frame, width=30)
        root.author_search_entry.pack(side='left', padx=5)
        ttk.Button(search_frame, text="Search", command = root.search_by_author).pack(side='left', padx=0)
        ttk.Button(search_frame, text="Clear", command=root.load_books).pack(side='left', padx=0)
       
        ttk.Label(search_frame, text="Search Title:").pack(side='left', padx=5)
        root.title_search_entry = ttk.Entry(search_frame, width=30)
        root.title_search_entry.pack(side='left', padx=5)
        ttk.Button(search_frame, text="Search", command=root.search_by_title).pack(side='left',padx=5)
        ttk.Button(search_frame, text="Clear", command=root.load_books).pack(side='left', padx=5)

        ttk.Button(btn, text="Add Book", command=root.add_book).pack(side='left', padx=5)
        ttk.Button(btn, text="Edit Book", command=root.edit_book).pack(side='left', padx=5)
        ttk.Button(btn, text="Delete Book", command=root.delete_book).pack(side='left', padx=5)
        ttk.Button(btn, text="Refresh", command=root.load_books).pack(side='left', padx=5)
        # ttk.Button(btn, text="Search for Book Title", command=root.search_title).pack(side='left')

        root.load_books()

    def search_by_title(root):
        search_term = root.title_search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a title to search")
            return
        
        try:
            root.book_tree.delete(*root.book_tree.get_children())

            books = root.db.execute_query("""
                SELECT book_id, title, author_first_name, author_last_name, genre, publication_year, total_copies, available_copies
                FROM Book_Inventory
                WHERE title LIKE ?
                ORDER BY title
            """, (f"%{search_term}%",)).fetchall()

            if not books:
                messagebox.showinfo("No Results", "No books found with searched title")
                return
            
            for book in books:
                root.book_tree.insert('', 'end', values=book)

        except Exception as e:
            messagebox.showerror("Database Error", f"Search failed:\n{str(e)}")

    def search_by_author(root):
        search_term = root.author_search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter an author name to search")
            return
        
        try:
            root.book_tree.delete(*root.book_tree.get_children())

            books = root.db.execute_query("""
                SELECT book_id, title, author_first_name, author_last_name,
                    genre, publication_year, total_copies, available_copies
                FROM Book_Inventory
                WHERE author_first_name LIKE ? OR author_last_name LIKE ?
                ORDER BY author_last_name, author_first_name, title
            """, (f"%{search_term}%", f"%{search_term}%")).fetchall()

            if not books:
                messagebox.showinfo("No results", "No books found by searched author")
                return
            
            for book in books:
                root.book_tree.insert('', 'end', values=book)

        except Exception as e:
            messagebox.showerror("Database Error", f"Search failed:\n{str(e)}")

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
            ("Title*:", "title"),
            ("Author First Name*:", "author_first_name"),
            ("Author Last Name*:", "author_last_name"),
            ("Genre:", "genre"),
            ("Publication Year:", "publication_year"),
            ("Total Copies*:", "total_copies"),
            ("Available Copies*:", "available_copies")
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
            messagebox.showwarning("Warning", "Please select a book to edit")
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

    def setup_customer_tab(root, frame):
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(tree_frame)
        scroll_y.pack(side='right', fill='y')


        cols = ("Customer ID", "First Name", "Last Name", "Email", "Phone", "Date Joined", "Status")
        root.customer_tree = ttk.Treeview(
            tree_frame,
            columns=cols,
            show='headings',
            yscrollcommand=scroll_y.set,
            selectmode='browse'
        )
        scroll_y.config(command=root.customer_tree.yview)
        col_widths = [75, 100, 100, 150, 120, 60, 60, 80]
        for col, width in zip(cols, col_widths):
            root.customer_tree.heading(col, text=col)
            root.customer_tree.column(col, width=width, anchor='center')

        root.customer_tree.pack(fill='both', expand=True)

        btn = ttk.Frame(frame)
        btn.pack(pady=10)

        ttk.Button(btn, text="Add Customer", command=root.add_customer).pack(side='left', padx=5)
        ttk.Button(btn, text="Edit Customer", command=root.edit_customer).pack(side='left', padx=5)
        ttk.Button(btn, text="Archive Customer", command=root.archive_customer).pack(side='left', padx=5)
        ttk.Button(btn, text="Reactivate Customer", command=root.reactivate_customer).pack(side='left', padx=5)
        ttk.Button(btn, text="Delete Customer", command=root.delete_customer).pack(side='left', padx=5)
        ttk.Button(btn, text="Refresh", command=root.load_customers).pack(side='left', padx=5)


        root.load_customers()

    def reactivate_customer(root):
        selected = root.customer_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a customer to reactivate")

        customer_id = root.customer_tree.item(selected,'values')[0]
        if messagebox.askyesno("Confirm", "Reactivate this customer?"):
            try:
                root.db.execute_query("""
                    UPDATE Customer_Details
                    SET status = 'Active'
                    WHERE customer_id = ?
                """, (customer_id,))
                root.db.conn.commit()
                root.load_customers()
            except Exception as e:
                messagebox.showerror("Error", f"Could not reactivate customer:\n{str(e)}")

    def delete_customer(root):
        selected = root.customer_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a custo,er to delete")
            return

        customer_id = root.customer_tree.item(selected, 'values')[0]
        if messagebox.askyesno("Confirm", "Delete this customer permanently?"):
            try:
                root.db.execute_query("DELETE FROM Customer_Details WHERE customer_id=?",(customer_id,))
                root.db.conn.commit()
                root.load_customers()
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete customers:\n{str(e)}")

    def load_customers(root):
        try:
            root.customer_tree.delete(*root.customer_tree.get_children())

            customers = root.db.execute_query("""
                SELECT customer_id, first_name, last_name, email_address, phone_number, date_joined, status
                FROM Customer_Details
                ORDER BY customer_id
            """).fetchall()

            for customer in customers:
                root.customer_tree.insert('', 'end', values=customer)

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load customers:\n{str(e)}")

    def add_customer(root, customer_data=None):
        dialog = tk.Toplevel(root)
        dialog.title("Add New Customer" if not customer_data else "Edit Customer")
        dialog.resizable(False, False)

        fields = [
            ("First Name*:", "first_name"),
            ("Last Name*:", "last_name"),
            ("Email:", "email_address"),
            ("Phone*:", "phone_number"),
            ("Today's Date:", "date_joined"),
            ("Status:", "status")
        ]

        entries = {}
        for row, (label, name) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=row, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(dialog)
            entry.grid(row=row, column=1, padx=5, pady=5)

            if not customer_data:
                if name == "date_joined":
                    entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
                    entry.config(state='readonly')
                
                elif name == "status":
                    entry.insert(0, "Active")
                    entry.config(state='readonly')

            if customer_data:
                entry.insert(0, customer_data[row+1])
            entries[name]=entry

        submit_text = "Add Customer" if not customer_data else "Update"
        ttk.Button(
            dialog,
            text=submit_text,
            command=lambda: root.save_customer(
                entries,
                dialog,
                customer_data[0] if customer_data else None
            )
        ).grid(row=len(fields), columnspan=2, pady=10)

    def save_customer(root, entries, dialog, customer_id=None):
        try:
           # total_copies = int(entries['total_copies'].get())
            #available_copies = int(entries['available_copies'].get())

            #if available_copies > total_copies:
             #   raise ValueError("Available copies cannot exceed total copies")
            
            data = (
                entries['first_name'].get(),
                entries['last_name'].get(),
                entries['email_address'].get(),
                entries['phone_number'].get(),
                entries['date_joined'].get(),
                entries['status'].get()
            )

            if customer_id:
                root.db.execute_query("""
                    UPDATE Customer_Details
                    SET first_name=?, last_name=?, email_address=?, phone_number=?, date_joined=?, status=?
                    WHERE customer_id=?
                """, (*data, customer_id))
            else:
                root.db.execute_query("""
                    INSERT INTO Customer_Details (first_name, last_name, email_address, phone_number, date_joined, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, data)

                root.db.conn.commit()
                root.load_customers()
                dialog.destroy()
                messagebox.showinfo("Success", "Customer saved successfully")
        
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Database Error", f"Operation failed: {str(e)}")        

    def archive_customer(root):
        selected = root.customer_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a customer to archive")
            return
        
        customer_id = root.customer_tree.item(selected, 'values')[0]
        if messagebox.askyesno("Confirm", "Archive this customer?"):
            try:
                root.db.execute_query("""
                    UPDATE Customer_Details
                    SET status = 'Inactive'
                    WHERE customer_id=?
                """, (customer_id,))
                root.db.conn.commit()
                root.load_customers()
            except Exception as e:
                messagebox.showerror("Error", f"Could not archive customer:\n{str(e)}")

    def edit_customer(root):
        selected = root.customer_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select customer to edit")
            return
        
        customer_data = root.customer_tree.item(selected, 'values')
        root.add_customer(customer_data)

    def setup_transaction_tab(root, frame):
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        scroll_y=ttk.Scrollbar(tree_frame)
        scroll_y.pack(side='right', fill='y')

        cols = ("Transaction ID", "Customer ID", "Book ID", "Checkout Date", "Due Date", "Return Date", "Status")
        root.transaction_tree = ttk.Treeview(
            tree_frame,
            columns=cols,
            show='headings',
            yscrollcommand=scroll_y.set,
            selectmode='browse'
        )
        scroll_y.config(command=root.transaction_tree.yview)
        col_widths = [75, 75, 75, 150, 150, 150, 75]
        for col, width in zip(cols, col_widths):
            root.transaction_tree.heading(col, text=col)
            root.transaction_tree.column(col, width=width, anchor='center')

        root.transaction_tree.pack(fill='both', expand=True)

        root.details_frame = ttk.LabelFrame()

        btn = ttk.Frame(frame)
        btn.pack(pady=10)

        ttk.Button(btn, text="Check In Book", command=root.checkin_book).pack(side='left', padx=5)
        ttk.Button(btn, text="Check Out Book", command=root.show_checkout_dialog).pack(side='left', padx=5)
        ttk.Button(btn, text="View Details", command=root.show_transaction_details).pack(side='left', padx=5)
        ttk.Button(btn, text="Refresh", command=root.load_customers).pack(side='left', padx=5)

        root.load_transactions()

    def show_transaction_details(root):
        try:
            selected = root.transaction_tree.focus()
            if not selected:
                messagebox.showwarning("Warning", "Please select a transaction to view")
                return
            
            transaction_id = root.transaction_tree.item(selected)['values'][0]

            details = root.db.execute_query("""
                SELECT 
                    t.transaction_id, t.checkout_date, t.due_date, 
                    t.return_date, t.status,
                    b.title, b.author_first_name || ' ' || b.author_last_name as author,
                    c.first_name || ' ' || c.last_name as customer,
                    c.email_address, c.phone_number
                FROM Transactions t
                JOIN Book_Inventory b ON t.book_id = b.book_id
                JOIN Customer_Details c ON t.customer_id = c.customer_id
                WHERE t.transaction_id = ?
            """, (transaction_id,)).fetchone()

            if not details:
                messagebox.showerror("Error", "Transaction details not found")
                return

            dialog = tk.Toplevel(root)
            dialog.title(f"Transaction #{transaction_id} Details")
            dialog.geometry("300x350")

            fields = [
                ("Transaction ID:", details[0]),
                ("Book:", details[5]),
                ("Author:", f"{details[6]}"),
                ("Customer:", f"{details[7]}"),
                ("Email:", details[8]),
                ("Phone:", details[9]),
                ("Checkout Date:", details[1]),
                ("Due Date:", details[2]),
                ("Return Date:", details[3] if details[3] else "Not Returned"),
                ("Status:", details[4])
            ]

            for row, (label, value) in enumerate(fields):
                ttk.Label(dialog, text=label). grid(row=row, column=0, sticky='e', padx=5, pady=5)
                ttk.Label(dialog, text=value).grid(row=row, column=1, sticky='w', padx=5, pady=5)

            ttk.Button(dialog, text="Close", command=dialog.destroy).grid(row=len(fields), columnspan=2, pady=10)

            if details[4] == 'Checked Out':
                btn = ttk.Frame(dialog)
                btn.grid(row=len(fields), columnspan=2, pady=10)

                ttk.Button(btn, text="Check In", command= root.checkin_book).pack(side='left', padx=5)
                ttk.Button(btn, text="Close", command=dialog.destroy).pack(side='left', padx=5)
            else:
                ttk.Button(dialog, text="Close", command=dialog.destroy).grid(row=len(fields), columnspan=2, pady=10)

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load details:\n{str(e)}")
            
    def load_transactions(root):
        try:
            root.transaction_tree.delete(*root.transaction_tree.get_children())

            transactions = root.db.execute_query("""
                SELECT transaction_id, customer_id, book_id, checkout_date, due_date, return_date, status
                FROM Transactions
                ORDER BY transaction_id
            """).fetchall()

            for transaction in transactions:
                root.transaction_tree.insert('', 'end', values=transaction)

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load Transactions:\n{str(e)}")

    def checkin_book(root):
        selected = root.transaction_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to check in")
            return
        
        if selected:
            item = root.transaction_tree.item(selected)
            status = item['values'][6]

            transaction_id = item['values'][0]
            cur = root.db.execute_query("SELECT status FROM Transactions WHERE transaction_id=?",(transaction_id,))
            result = cur.fetchone()
            if result and result[0] == 'Returned':
                messagebox.showerror("Error", "Book already checked in")
                return False 
            
            book_id = item['values'][2]
            cur = root.db.execute_query("""
                SELECT title
                FROM Book_Inventory bi
                JOIN Transactions t ON t.book_id = bi.book_id
                WHERE bi.book_id = ?
            """, (book_id,)).fetchone()
            book_title = cur[0]

            if not messagebox.askyesno("Confirm Check In?", f"Check in book: {book_title} (ID = {book_id})?"):
                return
            
            try:
                root.db.execute_query("""
                    UPDATE Transactions
                    SET return_date = DATE('now')
                    WHERE transaction_id = ?
                """,(transaction_id,))

                root.db.execute_query("""
                    UPDATE Book_Inventory
                    SET available_copies = available_copies+1
                    WHERE book_id = ?
                """,(book_id,))

                root.db.execute_query("""
                    UPDATE Transactions
                    SET status = 'Returned'
                    WHERE transaction_id = ?
                """,(transaction_id,))

                root.db.execute_query("""
                    DELETE FROM Checked_Out_Books
                    WHERE transaction_id = ?
                """, (transaction_id,))

                root.db.conn.commit()

                messagebox.showinfo("Success", f"'{book_title} (ID = {book_id})' has been checked in")
                root.load_transactions()
                root.load_books()
                root.load_checkout_books()

            except Exception as e:
                root.db.conn.rollback()
                messagebox.showerror("Database Error", f"Error: {str(e)}")

    def show_checkout_dialog(root):
        root.dialog = tk.Toplevel(root)
        root.dialog.title("Check Out Book")
        root.dialog.geometry("300x150")

        default_due = (datetime.now() + timedelta(days=28)).strftime('%Y-%m-%d')

        ttk.Label(root.dialog, text="Book:").grid(row=0, column=0, padx=5, pady=5)
        root.book_combo = ttk.Combobox(root.dialog, state='readonly')
        root.book_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root.dialog, text="Customer:").grid(row=1, column=0, padx=5, pady=5)
        root.customer_combo = ttk.Combobox(root.dialog, state='readonly')
        root.customer_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root.dialog, text="Due Date:").grid(row=2, column=0, padx=5, pady=5)
        root.due_date_entry = ttk.Entry(root.dialog)
        root.due_date_entry.insert(0, default_due)
        root.due_date_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(root.dialog, text="Submit", command=root.process_checkout).grid(row=3, columnspan=2, pady=10)
        root.load_available_books()
        root.load_active_customers()

    def process_checkout(root):
        try:
            book_text = root.book_combo.get()
            if not book_text:
                messagebox.showwarning("Warning", "Please select a book to check out")
                return
            
            book_id = int(book_text.split('(ID: ')[1].rstrip(')'))

            cust_text = root.customer_combo.get()
            if not cust_text:
                messagebox.showwarning("Warning", "Please select a customer")
                return
            
            customer_id = int(cust_text.split('(ID: ')[1].rstrip(')'))

            due_date = root.due_date_entry.get()
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                messagebox("Error", "Invalid date formate. Use YYYY-MM-DD")
                return
            
            if not messagebox.askyesno("Confirm", "Process this checkout?"):
                return
            
            checkout_date = datetime.now().strftime('%Y-%m-%d')

            root.db.execute_query("""
                INSERT INTO Transactions
                (customer_id, book_id, checkout_date, due_date, status)
                VALUES (?, ?, ?, ?, 'Checked Out')
            """,(customer_id, book_id, checkout_date, due_date))

            root.db.execute_query("""
                UPDATE Book_Inventory
                SET available_copies = available_copies - 1
                WHERE book_id = ?
            """, (book_id,))

            root.db.execute_query("""
                INSERT INTO Checked_Out_Books
                (transaction_id, customer_id, book_id, checkout_date, due_date)
                SELECT last_insert_rowid(), ?, ?, ?, ?
            """, (customer_id, book_id, checkout_date, due_date))

            root.db.conn.commit()

            messagebox.showinfo("Success", "Book checked out successfully")
            #dialog.destroy()
            root.load_transactions()
            root.load_books()
            root.load_checkout_books()
        
        except Exception as e:
            root.db.conn.rollback()
            messagebox.showerror("Error", f"Checkout failed: {str(e)}")

    def load_available_books(root):
        try:
            books = root.db.execute_query("""
                SELECT book_id, title
                FROM Book_Inventory
                WHERE available_copies > 0
                ORDER BY title
            """).fetchall()

            root.book_combo['values'] = [f"{title} (ID: {id})" for id, title in books]
            if books:
                root.book_combo.current(0)
            #root.book_combo.set('Select a book')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load books: {str(e)}")

    def load_active_customers(root):
        try:
            customers = root.db.execute_query("""
                SELECT customer_id, first_name, last_name 
                FROM Customer_Details 
                WHERE status = 'Active'
                ORDER BY last_name
            """).fetchall()

            root.customer_combo['values'] = [f"{first} {last} (ID: {id})" for id, first, last in customers]
            if customers:
                root.customer_combo.current(0)            
            #root.customer_combo.set('Select a customer')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customers: {str(e)}")  

    def setup_checkedout_tab(root, frame):
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(tree_frame)
        scroll_y.pack(side='right', fill='y')


        cols = ("Checkout ID", "Transaction ID", "Customer ID", "Book ID", "Checkout Date", "Due Date")
        root.checkout_tree = ttk.Treeview(
            tree_frame,
            columns=cols,
            show='headings',
            yscrollcommand=scroll_y.set,
            selectmode='browse'
        )
        scroll_y.config(command=root.checkout_tree.yview)
        col_widths = [75, 100, 100, 150, 120, 60, 60, 80]
        for col, width in zip(cols, col_widths):
            root.checkout_tree.heading(col, text=col)
            root.checkout_tree.column(col, width=width, anchor='center')

        root.checkout_tree.pack(fill='both', expand=True)

        btn = ttk.Frame(frame)
        btn.pack(pady=10)

        ttk.Button(btn, text="Get Check Out Information", command=root.checkout_info).pack(side='left', padx=5)
        ttk.Button(btn, text="Refresh", command=root.load_checkout_books).pack(side='left', padx=5)

        root.load_checkout_books()

    def checkout_info(root):
        try:
            selected = root.checkout_tree.focus()
            if not selected:
                messagebox.showwarning("Warning", "Please select a checkout to view")
                return
            
            checkout_id = root.checkout_tree.item(selected)['values'][0]

            details = root.db.execute_query("""
                SELECT 
                    ch.checkout_id, ch.checkout_date, ch.due_date, ch.transaction_id, ch.customer_id, ch.book_id,
                    c.first_name || ' ' || c.last_name as customer, c.phone_number, c.email_address,
                    b.title, b.author_first_name || ' ' || b.author_last_name as author
                FROM Checked_Out_Books ch
                JOIN Customer_Details c ON c.customer_id = ch.customer_id
                JOIN Book_Inventory b on b.book_id = ch.book_id
                WHERE checkout_id = ?
            """, (checkout_id,)).fetchone()

            if not details:
                messagebox.showerror("Error", "Checkout details not found")
                return

            dialog = tk.Toplevel(root)
            dialog.title(f"Transaction #{checkout_id} Details")
            dialog.geometry("300x400")

            fields = [
                ("Checkout ID:", details[0]),
                ("Transaction ID:", details[3]),
                ("Book:", details[9]),
                ("Book ID:", details[5]),
                ("Author:", f"{details[10]}"),
                ("Customer:", f"{details[6]}"),
                ("Customer ID:", details[4]),
                ("Email:", details[8]),
                ("Phone:", details[7]),
                ("Checkout Date:", details[1]),
                ("Due Date:", details[2]),
            ]

            for row, (label, value) in enumerate(fields):
                ttk.Label(dialog, text=label). grid(row=row, column=0, sticky='e', padx=5, pady=5)
                ttk.Label(dialog, text=value).grid(row=row, column=1, sticky='w', padx=5, pady=5)

            ttk.Button(dialog, text="Close", command=dialog.destroy).grid(row=len(fields), columnspan=2, pady=10)

            if details[4] == 'Checked Out':
                btn = ttk.Frame(dialog)
                btn.grid(row=len(fields), columnspan=2, pady=10)

                ttk.Button(btn, text="Check In", command= root.checkin_book).pack(side='left', padx=5)
                ttk.Button(btn, text="Close", command=dialog.destroy).pack(side='left', padx=5)
            else:
                ttk.Button(dialog, text="Close", command=dialog.destroy).grid(row=len(fields), columnspan=2, pady=10)

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load details:\n{str(e)}")
            
    def load_checkout_books(root):
        try:
            root.checkout_tree.delete(*root.checkout_tree.get_children())

            checkouts = root.db.execute_query("""
                SELECT checkout_id, transaction_id, customer_id, book_id, checkout_date, due_date
                FROM Checked_Out_Books
                ORDER BY checkout_id
            """).fetchall()

            for checkout in checkouts:
                root.checkout_tree.insert('', 'end', values=checkout)

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load checked out books:\n{str(e)}")

    #def checkout_info(root):
        return
    
    #def checkin_book(root):
        return

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
