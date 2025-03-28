# Vulnerable Website for Penetration Testing

This is a basic website created for penetration testing purposes. It contains intentional vulnerabilities for educational purposes.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the server:
```bash
npm start
```

3. Visit http://localhost:3000 in your browser

4. Install `DevDb` extension in VS Code if you want to view the contents of users.db (SQLLite database) alongside the code.

## Features

- User registration
- User login
- Profile viewing
- Profile Editing
- SQLite database storage

## Security Vulnerabilities

This website contains several intentional security vulnerabilities for penetration testing purposes:

1. SQL Injection vulnerabilities in all database queries
2. Plain text password storage
3. No input validation
4. No password complexity requirements
5. No rate limiting
6. No CSRF protection
7. No XSS protection
8. No secure session configuration
9. Many more! 

## Note

This website is intentionally vulnerable and it's only used for a pentest.