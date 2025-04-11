import sqlite3
con = sqlite3.connect("Library.db")
cur = con.cursor()

#insert books to Book_Inventory table

new_books =[
    ("Interview with the Vampire", "Anne Rice", "Gothic Horror", 6, 5),
    ("Paper Towns", "John Green", "Young Adult Fiction", 3, 3),
    ("Rebecca", "Daphne de Maurier", "Gothic Horror", 1, 1),
    ("1984", "George Orwell", "Fiction", 2, 2),
    ("Twilight", "Stephanie Meyer", "Fiction", 6,6),
    ("The Master and Margarita", "Mikhail Bulgakov", "Fiction", 1, 1),
    ("The Picture of Dorian Gray", "Oscar Wilde", "Gothic Fiction", 2, 1),
    ("The Stranger", "Albert Camus", "Fiction", 3,3),
    ("YOU", "Caroline Kepnes", "Fiction", 2, 2),
    ("The Shining", "Stephen King", "Horror", 5, 5),
    ("Dracula", "Bram Stoker", "Horror", 3, 3),
    ("Jane Eyre", "Charlotte Bronte", "Classic Fiction", 1, 0)
]

cur.executemany("INSERT INTO Book_Inventory (title, author_first_name, author_last_name, genre, total_copies, available_copies) VALUES (?, ?, ?, ?, ?, ?)", new_books)
con.commit()

#insert customers into Customer_Details table

new_customers = [
    ("James Wilson", "jameswilson@gmail.com", "123-456-7890", "03/12/23", "Active"),
    ("John Doe", "johndoe@gmail.com", "368-265-9837", "06/01/2020", "Active"),
    ("Jane Doe", "janedoe@hotmail.com", "737-837-2847", "12/25/2015", "Inactive"),
    ("Claire Smith", "clairesmith22@aol.com", "847-923-1234", "09/29/24", "Active"),
    ("Alex Smith", "alexsmith10@gmail.com", "736-938-9876", "05/11/2014", "Inactive"),
    ("Daniel Craig", "danielgraig@gmail.com", "627-999-2736", "01/22/2025", "Active"),
    ("Holly Jones", "hollyjones77@gmail.com", "738-111-2837", "02/01/2018", "Inactive")
]

cur.executemany("INSERT INTO Customer_Details (first_name, last_name, email_address, phone_number, date_joined, status) VALUES (?, ?, ?, ?, ?, ?)", new_customers)
con.commit()

# insert transactions

transaction_data = [
    (1, 2, "04/22/2025", "05/22/2025", "Returned"),
    (7, 3, "09/22/2018", "10/22/2018", "Returned"),
    (4, 9, "10/01/2024", "11/01/2024", "Returned"),
    (2, 1, "02/11/2024", "03/11/2024", "Returned"),
    (4, 7, "03/29/2025", "04/29/2025", "Checked Out"),
    (4, 1, "03/29/2025", "04/29/2025", "Checked Out"),
    (1, 12, "03/13/2025", "04/13/2025", "Checked Out")
]

cur.executemany("INSERT INTO Transactions (customer_id, book_id, checkout_date, due_date, status) VALUES (?, ?, ?, ?, ?)", transaction_data)
con.commit()

# insert checked out books

checkedout_books_data = [
    (4, 1, "03/29/2025", "04/29/2025"),
    (1, 12, "03/13/2025", "04/13/2025"),
    (4, 7, "03/29/2025", "04/29/2025")
]

cur.executemany("INSERT INTO Checked_Out_Books (customer_id, book_id, checkout_date, due_date) VALUES (?, ?, ?, ?)", checkedout_books_data)
con.commit()

con.close()