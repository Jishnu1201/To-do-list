DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS list;

CREATE TABLE list (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       task TEXT,
       created DATETIME,
       due DATETIME,
       status TEXT,
       description TEXT
);      

       
