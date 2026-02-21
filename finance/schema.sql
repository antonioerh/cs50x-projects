CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    username TEXT NOT NULL, hash TEXT NOT NULL, 
    cash NUMERIC NOT NULL DEFAULT 10000.00
);

CREATE TABLE stocks (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    price FLOAT NOT NULL,
    total FLOAT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE transactions (
    transaction_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,
    symbol TEXT NOT NULL,
    shares TEXT NOT NULL,
    proceeds FLOAT NOT NULL,
    date TEXT NOT NULL, price FLOAT,
    PRIMARY KEY (transaction_id)
);