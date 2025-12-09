// backend/server.js
const express = require('express');
const mysql = require('mysql');
const cors = require('cors');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// MySQL connection (uses user we created: appuser / app_pass_123)
const db = mysql.createConnection({
  host: 'localhost',
  user: 'appuser',
  password: 'app_pass_123',
  database: 'crud',
});

// Connect and log result
db.connect((err) => {
  if (err) {
    console.error('❌ DB CONNECTION ERROR:', err);
  } else {
    console.log('✅ MySQL connected');
  }
});

// Health check
app.get('/', (req, res) => {
  res.send('API is running');
});

// LOGIN ENDPOINT
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  console.log('🔐 Login attempt:', username, password);

  if (!username || !password) {
    return res.status(400).json({ message: 'Missing username or password' });
  }

  const sql = 'SELECT * FROM login WHERE username = ? AND password = ?';

  db.query(sql, [username, password], (err, rows) => {
    if (err) {
      console.error('❌ DB QUERY ERROR (login):', err);
      return res.status(500).json({
        message: 'Database error',
        error: err.code || err.message,
      });
    }

    if (rows.length > 0) {
      console.log('✅ Login Successful for:', username);
      return res.json({ message: 'Login Successfully' });
    } else {
      console.log('❌ No matching record for:', username);
      return res.status(401).json({ message: 'No Record' });
    }
  });
});

// SIGNUP ENDPOINT
app.post('/signup', (req, res) => {
  const { username, password } = req.body;
  console.log('📝 Signup attempt:', username, password);

  if (!username || !password) {
    return res.status(400).json({ message: 'Missing username or password' });
  }

  // 1) Check if user already exists
  const checkSql = 'SELECT id FROM login WHERE username = ?';

  db.query(checkSql, [username], (err, rows) => {
    if (err) {
      console.error('❌ DB QUERY ERROR (check user):', err);
      return res.status(500).json({ message: 'Database error' });
    }

    if (rows.length > 0) {
      // user already exists
      return res.status(409).json({ message: 'User already exists' });
    }

    // 2) Insert new user
    const insertSql = 'INSERT INTO login (username, password) VALUES (?, ?)';

    db.query(insertSql, [username, password], (err2, result) => {
      if (err2) {
        console.error('❌ DB QUERY ERROR (insert user):', err2);
        return res.status(500).json({ message: 'Database error' });
      }

      console.log('✅ User created with id:', result.insertId);
      return res.json({ message: 'Signup successful' });
    });
  });
});

// Start server
app.listen(8081, () => {
  console.log('🚀 Backend running at http://localhost:8081');
});
