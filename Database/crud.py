import sqlite3

def connect():
    return sqlite3.connect("Library.db")

# CREATE Functions

# add new books to library/ Books_Inventory
def add_book(title, author_name, genre, total_copies):
    con = connect()
    cur = con.cursor()
    cur.execute("INSERT INTO Book_Inventory (title, author_name, genre, total_copies, available_copies) VALUES (?, ?, ?, ?, ?)", 
                (title, author_name, genre, total_copies, total_copies))
    con.commit()
    con.close()

# add new customers to Customer_Details
def add_customer(name,email, phone, date_joined, status):
    con = connect()
    cur = con.cursor()
    cur.execute("INSERT INTO Customer_Details (name, email_address, phone_number, date_joined, status) VALUES (?, ?, ?, ?, ?)",
                (name, email, phone, date_joined, status) )
    con.commit()
    con.close()

# Create new transaction/ checking out a book
def create_transaction(customer_id, book_id, checkout_date, due_date):
    con = connect()
    cur = con.cursor()

    #check if book is available to checkout
    cur.execute("SELECT available_copies FROM Book_Inventory WHERE book_id = ?", (book_id,))
    book = cur.fetchone()

    if book[0] > 0:
        cur.execute("""
            INSERT INTO Transactions (customer_id, book_id, checkout_date, due_date, status)
            VALUES (?, ?, ?, ?, 'Checked Out')
        """, (customer_id, book_id, checkout_date, due_date))

        # add record to checkout_books table
        cur.execute("""
            INSERT INTO Checked_Out_Books (customer_id, book_id, checkout_date, due_date)
            VALUES (?, ?, ?, ?)
        """, (customer_id, book_id, checkout_date, due_date))

        # reduce available copies by 1
        cur.execute("UPDATE Book_Inventory SET available_copies = available_copies - 1 WHERE book_id = ?", (book_id,))
        con.commit()
    else:
        print(f"Book ID {book_id} is not available!")
    
    con.close()
 

# READ Functions

# Read / display all books at the library
def get_books():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM Book_Inventory")
    books = cur.fetchall()
    con.close()
    return books

# Read / display all customers at the library
def get_customers():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM Customer_Details")
    customers = cur.fetchall()
    con.close()
    return customers

# Read / display currently checked out books
def get_checked_out_books():
    con = connect()
    cur = con.cursor()
    cur.execute("""
        SELECT Transactions.transaction_id, Customer_Details.name, Book_Inventory.title, Transactions.checkout_date, Transactions.due_date
        FROM Transactions
        JOIN Customer_Details ON Transactions.customer_id = Customer_Details.customer_id
        JOIN Book_Inventory ON Transactions.book_id = Book_Inventory.book_id
        WHERE Transactions.status = 'Checked Out'
    """)
    checkouts = cur.fetchall()
    con.close()
    return checkouts
    

    

# UPDATE Functions

# Update number of total copies of a book (if you recieve a new copy or lose an old copy)
def update_books_available(book_id, new_available_copies):
    con = connect()
    cur = con.cursor()
    cur.execute("UPDATE Book_Inventory SET total_copies = ? WHERE book_id = ?", (new_available_copies, book_id))
    con.commit()
    con.close()

# update mark book as returned and update available_books
def mark_book_returned(transaction_id):
    con = connect()
    cur = con.cursor()

    # get returned book id from transaction
    cur.execute("SELECT book_id FROM Transactions WHERE transaction_id = ?", (transaction_id, ))
    book = cur.fetchone()

    if book:
        book_id = book[0]
            
        # Update transaction record in Transactions table
        cur.execute("UPDATE Transactions SET status = 'Returned' WHERE transaction_id = ?",
                    (transaction_id,))
        
        cur.execute("DELETE FROM Checked_Out_Books WHERE book_id = ?", (book_id,))
            
        # update available copies
        cur.execute("UPDATE Book_Inventory SET available_copies = available_copies + 1 WHERE book_id = ?", (book_id,))

        con.commit()
    con.close()

# DELETE

# Delete book from Book_Inventory for when they stop carrying a book
def delete_book(book_id):
    con = connect()
    cur = con.cursor()
    cur.execute("DELETE FROM Book_Inventory WHERE book_id = ?", (book_id,))
    con.commit()
    con.close()


 # Delete a customer
def delete_customer(customer_id):
    con = connect()
    cur = con.cursor()
    cur.execute("DELETE FROM Customer_Details WHERE customer_id = ?", (customer_id,))
    con.commit()
    con.close()


# Test CRUD Functions
if __name__ == "__main__":

    # Test create 
    add_book('Brave New World', 'Aldous Huzley', 'Dystopian', 4)

    add_customer("Alice Johnson", "alicejohnson33@gmail.com", "324-334-5532", "03/30/2025", "Active")

    create_transaction(1, 5, "03/31/2025", "05/01/2025")


    # Test Read
    print ("All Books:")
    for book in get_books():
        print(book)
    
    print("All Customers:")
    for customer in get_customers():
        print(customer)

    print("Checked Out Books:")
    for checkout in get_checked_out_books():
       print(checkout)

    # Test Update

    update_books_available(1,5)

    mark_book_returned(6)

    # Test Delete
    delete_book(9)

    delete_customer(3)