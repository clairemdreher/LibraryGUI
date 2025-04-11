-- CREATE

-- Create a new book / add a new book to the library
INSERT INTO Book_Inventory (title, author_first_name, author_last_name, genre, publication_year, total_copies, available_copies)
VALUES ('Brave New World', 'Aldous', 'Huxley', 'Dystopian Fiction', 1932, 1, 1);


-- Create a new customer / add new customer
INSERT INTO Customer_Details (first_name, last_name, email_address, phone_number, date_joined, status)
VALUES ('Greg', 'House', 'greghouse@house.com', '111-111-1111', '2025-03-31', 'Active');


-- Create a transaction / check out a book
-- check if book is available
SELECT available_copies FROM Book_inventory WHERE book_id = 3;
-- if available, create a new transaction
INSERT INTO Transactions(customer_id, book_id, checkout_date, due_date, return_date, status)
VALUES (6, 3, '2025-03-31', '2025-05-01', NULL, 'Checked Out');
-- add to Checked_Out_Books table to show customer 6 has book 3 checked out
INSERT INTO Checked_Out_Books (transaction_id, customer_id, book_id, checkout_date, due_date)
VALUES (last_insert_rowid(), 6, 3, '2025-03-31', '2025-05-01');
-- decrease available copies in Book_Inventory by 1
UPDATE Book_Inventory
SET available_copies = available_copies -1
WHERE book_id = 3;



-- READ

-- Read / display all books
SELECT * FROM Book_Inventory;
-- Read title and author_name of book_id = 11
SELECT title, author_name FROM Book_Inventory WHERE book_id = 11;


-- Read / display all customer
SELECT * FROM Customer_Details;
-- Read name and status of customer_id = 3
SELECT name, status FROM Customer_Details WHERE customer_id = 3;

-- Read / display all books currently checked out
SELECT Transactions.transaction_id, Customer_Details.first_name, Customer_Details.last_name, Book_Inventory.title, Transactions.checkout_date, Transactions.due_date
FROM Transactions
JOIN Customer_Details ON Transactions.customer_id = Customer_Details.customer_id
JOIN Book_Inventory ON Transactions.book_id = Book_Inventory.book_id
WHERE Transactions.status = 'Checked Out';


-- UPDATE

-- update the total copies of a book, if one is lost or damaged for example
UPDATE Book_Inventory
SET available_copies = available_copies - 1,
    total_copies = total_copies - 1
WHERE book_id = 1;


-- update transaction when book is returned / mark book as returned
-- update transactions record marked as returned
UPDATE Transactions
SET status = 'Returned'
WHERE transaction_id = 5;
-- update return_date in Transactions
UPDATE Transactions
SET return_date = '2025-03-31'
WHERE transaction_id = 5;
-- delete entry from Checked_Out_Books
DELETE FROM Checked_Out_Books
WHERE book_id = 7;
-- increase available copies after return
UPDATE Book_Inventory
SET available_copies = available_copies + 1
WHERE book_id = 7;


--DELETE

-- delete a book from the inventory
DELETE FROM Book_Inventory
WHERE book_id = 9;

-- delete a customer
DELETE FROM Customer_Details 
WHERE customer_id = 3;

