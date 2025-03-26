CREATE DATABASE IF NOT EXISTS vuln_db;
USE vuln_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert some test data
INSERT INTO users (username, password) VALUES 
('admin', 'admin123'),
('user1', 'password123');

INSERT INTO products (name, price) VALUES 
('Product 1', 99.99),
('Product 2', 149.99),
('Product 3', 199.99); 