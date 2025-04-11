-- Insert rows into Book_Inventory
INSERT INTO Book_Inventory (title, author_name, isbn, genre, publication_year, total_copies, available_copies)
VALUES 
    ('Interview with the Vampire', 'Anne Rice','0345337662', 'Gothic Horror', 1976, 6, 5),
    ('Paper Towns', 'John Green', '0142414934', 'Young Adult Fiction', 2008, 3, 3),
    ('Rebecca', 'Daphne de Maurier', '0380730405', 'Gothic Horror', 1938, 1, 1),
    ('1984', 'George Orwell', '1443434973', 'Fiction', 1949, 2, 2),
    ('Twilight', 'Stephanie Meyer', '0316015849', 'Fiction', 2005, 6, 6),
    ('The Master and Margarita', 'Mikhail Bulgakov', '0679760806 ', 'Fiction', 1973, 1, 1),
    ('The Picture of Dorian Gray', 'Oscar Wilde', '1515190994', 'Gothic Fiction', 1891, 2, 1),
    ('The Stranger', 'Albert Camus', '0679720201', 'Fiction', 1942, 3, 3),
    ('YOU', 'Caroline Kepnes', '1476785608', 'Fiction', 2014, 2, 2),
    ('The Shining', 'Stephen King', '0307743659', 'Horror', 1977, 5, 5),
    ('Dracula', 'Bram Stoker', '1503261387', 'Horror', 1897, 3, 3),
    ('Jane Eyre', 'Charlotte Bronte', '0141441146', 'Classic Fiction', 1847, 1, 0);

-- Insert rows into Customer_Details
INSERT INTO Customer_Details (name, email_address, phone_number, date_joined, status)
VALUES
    ('James Wilson', 'jameswilson@gmail.com', '123-456-7890', '2023-12-03', 'Active'),
    ('John Doe', 'johndoe@gmail.com', '368-265-9837', '2020-06-01', 'Active'),
    ('Jane Doe', 'janedoe@hotmail.com', '737-837-2847', '2015-12-25', 'Inactive'),
    ('Claire Smith', 'clairesmith22@aol.com', '847-923-1234', '2024-09-29', 'Active'),
    ('Alex Smith', 'alexsmith10@gmail.com', '736-938-9876', '2014-05-11', 'Inactive'),
    ('Daniel Craig', 'danielgraig@gmail.com', '627-999-2736', '2025-01-22', 'Active'),
    ('Holly Jones', 'hollyjones77@gmail.com', '738-111-2837', '2018-02-01', 'Inactive');

--Insert rows into Transactions
INSERT INTO Transactions (customer_id, book_id, checkout_date, due_date, return_date, status)
VALUES
    (1, 2, '2025-04-22', '2025-05-22', '2025-05-15', "Returned"),
    (7, 3, '2018-09-22', '2018-10-22', '2025-10-01', "Returned"),
    (4, 9, '2024-10-01', '2024-11-01', '2024-10-29', "Returned"),
    (2, 1, '2024-02-11', '2024-03-11', '2024-03-11', "Returned"),
    (4, 7, '2025-03-29', '2025-04-29', NULL,"Checked Out"),
    (4, 1, '2025-03-29', '2025-04-29', NULL, "Checked Out"),
    (1, 12, '2025-03-13', '2025-04-13', NULL, "Checked Out");

-- Insert rows into Checked_Out_Books
INSERT INTO Checked_Out_Books (transaction_id, customer_id, book_id, checkout_date, due_date)
VALUES
    (6, 4, 1, '2025-03-29', '2025-04-29'),
    (7, 1, 12, '2025-03-13', '2025-04-13'),
    (5,4, 7, '2025-03-29', '2025-04-29');
