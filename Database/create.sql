-- Functional Dependencies:
-- book_id -> {title, author_name, isbn, genre, publication_year, total_copies, available_copies}
-- author name is only a property of the book in this case, author_name does not determine any other attribues, so no transitive dependencies
-- isbn is unique, so no partial dependencies

-- In my proposal, I had an attribute publisher_name, but that could cause transivtive dependency.
-- I had to remove the publisher_name attribute in this table, so that it is in 3NF
-- no transitive dependencies, so it is 3nf
CREATE TABLE Book_Inventory (
    book_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author_first_name TEXT NOT NULL,
    author_last_name TEXT NOT NULL,
    genre TEXT,
    publication_year YEAR,
    total_copies INTEGER NOT NULL,
    available_copies INTEGER NOT NULL
);

-- Functional Dependencies:
-- customer_id -> {name, email_address, phone_number, date_joined, status}

-- no transitive dependencies, so it is 3nf
CREATE TABLE Customer_Details (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email_address TEXT UNIQUE,
    phone_number TEXT NOT NULL,
    date_joined DATE NOT NULL,
    status TEXT NOT NULL CHECK(status in ('Active', 'Inactive'))
);

-- Functional Dependencies:
-- transaction_id -> {customer_id, book_id, checkout_date, due_date, return_date, status}

-- no transitive dependencies, so it is 3nf
CREATE TABLE Transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    checkout_date TEXT NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    status TEXT NOT NULL CHECK(status in ('Checked Out', 'Returned')),
    FOREIGN KEY (customer_id) REFERENCES Customer_Details(customer_id),
    FOREIGN KEY (book_id) REFERENCES Book_Inventory(book_id)
);

-- Functional Dependencies:
-- checkout_id -> {transaction_id, customer_id, book_id, checkout_date, due_date}

-- no transitive dependencies, so it is 3nf
CREATE TABLE Checked_Out_Books (
    checkout_id INTEGER PRIMARY KEY,
    transaction_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    checkout_date DATE NOT NULL,
    due_date DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customer_Details(customer_id),
    FOREIGN KEY (book_id) REFERENCES Book_Inventory(book_id) 
);

-- No foreign key constraints or triggers

-- In my proposal I mentioned that I would have a Fines table, but I decided to leave it out, because it was very complicated to implement since it depends on so many different attributes in different tables.
-- It was also left out so that I would have the needed 4 tables. 