const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const session = require('express-session');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const port = 3000;

// Database setup
const db = new sqlite3.Database('users.db', (err) => {
    if (err) {
        console.error(err.message);
    }
    console.log('Connected to the users database.');
});

// Create users table
db.run(`CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    email TEXT,
    full_name TEXT
)`);

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static('public'));
app.use(session({
    secret: 'mysecretkey',
    resave: false,
    saveUninitialized: true
}));

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/register', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'register.html'));
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.get('/profile', (req, res) => {
    if (!req.session.userId) {
        return res.redirect('/login');
    }
    res.sendFile(path.join(__dirname, 'public', 'profile.html'));
});

app.get('/edit-profile', (req, res) => {
    if (!req.session.userId) {
        return res.redirect('/login');
    }
    res.sendFile(path.join(__dirname, 'public', 'edit-profile.html'));
});

// API endpoints
app.post('/api/register', (req, res) => {
    const { username, password, email, full_name } = req.body;
    
    // Vulnerable: No input validation, SQL injection possible
    const sql = `INSERT INTO users (username, password, email, full_name) VALUES ('${username}', '${password}', '${email}', '${full_name}')`;
    
    db.run(sql, (err) => {
        if (err) {
            return res.status(400).json({ error: err.message });
        }
        res.json({ message: 'User registered successfully' });
    });
});

app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    
    // Vulnerable: SQL injection possible, plain text password comparison
    const sql = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
    
    db.get(sql, (err, row) => {
        if (err) {
            return res.status(400).json({ error: err.message });
        }
        if (row) {
            req.session.userId = row.id;
            res.json({ message: 'Login successful' });
        } else {
            res.status(401).json({ error: 'Invalid credentials' });
        }
    });
});

app.get('/api/profile', (req, res) => {
    if (!req.session.userId) {
        return res.status(401).json({ error: 'Not authenticated' });
    }
    
    // Vulnerable: SQL injection possible
    const sql = `SELECT * FROM users WHERE id = ${req.session.userId}`;
    
    db.get(sql, (err, row) => {
        if (err) {
            return res.status(400).json({ error: err.message });
        }
        res.json(row);
    });
});

app.post('/api/edit-profile', (req, res) => {
    if (!req.session.userId) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const { email, password, full_name } = req.body;

    // Vulnerable: No input validation, SQL injection possible
    let sql = `UPDATE users SET email = '${email}', full_name = '${full_name}'`;
    if (password) {
        sql += `, password = '${password}'`;
    }
    sql += ` WHERE id = ${req.session.userId}`;

    db.run(sql, (err) => {
        if (err) {
            return res.status(400).json({ error: err.message });
        }
        res.json({ message: 'Profile updated successfully' });
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});