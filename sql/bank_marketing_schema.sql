CREATE DATABASE IF NOT EXISTS bank_marketing_db;
USE bank_marketing_db;

DROP TABLE IF EXISTS bank_marketing_cleaned;

CREATE TABLE bank_marketing_cleaned (
    age INT NOT NULL,
    job VARCHAR(40),
    marital VARCHAR(20),
    education VARCHAR(40),
    default_status VARCHAR(10),
    balance INT,
    housing VARCHAR(10),
    loan VARCHAR(10),
    contact VARCHAR(20),
    day INT,
    month VARCHAR(10),
    duration INT,
    campaign INT,
    pdays INT,
    previous INT,
    poutcome VARCHAR(20),
    y VARCHAR(10)
);

-- Import the cleaned CSV using MySQL Workbench:
-- Server > Data Import > Table Data Import Wizard
-- Select data/cleaned/bank_marketing_cleaned.csv
-- Map the CSV column 'default' to the SQL column 'default_status'.
-- Alternatively, rename the CSV header 'default' to 'default_status' before import.
