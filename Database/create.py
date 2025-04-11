import sqlite3
con = sqlite3.connect("Library.db")
cur = con.cursor()

# In my proposal, I stated that I would have 5 tables, Book_Inventory, Customer_Details, Transactions, Checked_Out_Books, and Fines
# In my implementation, I have decided to drop the Fines table. The Fines table's implementation was very complicated and difficult to implement, so I decided to drop it.
# I also dropped it, so that I would have the nec


# Functional Dependencies:
# book_id uniquely determines title, author first name, author last name, genre, total_copies, available_copies
cur.execute("""
    CREATE TABLE IF NOT EXISTS Book_Inventory (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author_first_name TEXT NOT NULL,
        author_last_name TEXT NOT NULL,
        genre TEXT,
        total_copies INTEGER NOT NULL,
        available_copies INTEGER NOT NULL
    )
""")

# Functional Dependencies:
# customer_id uniquely determines first name, last name email_address, phone_numberm, date_joined, and status
cur.execute("""
    CREATE TABLE IF NOT EXISTS Customer_Details (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email_address TEXT,
        phone_number TEXT NOT NULL,
        date_joined TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status in ('Active', 'Inactive'))
    )
""")

# Functional Dependencies
# transaction_id uniquely determines customer_id, book_id, checkout_date, and due_date
cur.execute("""
    CREATE TABLE IF NOT EXISTS Transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        checkout_date TEXT NOT NULL,
        due_date TEXT,
        status TEXT NOT NULL CHECK(status in ('Checked Out', 'Returned')),
        FOREIGN KEY (customer_id) REFERENCES Customer_Details(customer_id),
        FOREIGN KEY (book_id) REFERENCES Book_Inventory(book_id)     
    )
""")

# Functional Dependencies
# checkout_id uniquely determines customer_id, book_id, checkout_date, and due_date
cur.execute("""
    CREATE TABLE IF NOT EXISTS Checked_Out_Books (
        checkout_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        checkout_date TEXT NOT NULL,
        due_date TEXT NOT NULL.
        FOREIGN KEY (customer_id) REFERENCES Customer_Details(customer_id),
        FOREIGN KEY (book_id) REFERENCES Book_Inventory(book_id)
    )
""")

con.close()