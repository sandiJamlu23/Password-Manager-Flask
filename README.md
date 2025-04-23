# 🛡️ Flask Password Manager

A simple, secure password manager built with Flask.  
It allows you to store, manage, and view your passwords with AES encryption.  

## Project Structures
password_manager_app/  
├── run.py                 # Main application entry point  
├── templates/             # HTML templates  
│   ├── base.html          # Base template  
│   ├── add.html           # Add password page  
│   ├── edit.html          # Edit password page  
│   ├── index.html         # Homepage (password list)  
│   ├── login.html         # Login page  
│   ├── register.html      # Registration page  
│   └── security.html      # Security settings page  
├── static/                # Static files (CSS, JS, images)  
│   ├── style.css          # Custom CSS  
│   └── password_strength.js  # JavaScript for password strength meter  
├── library.db             # SQLite database  
└── requirements.txt       # Python dependencies  
## 🚀 Features

- 🔐 Add, edit, and delete password entries
- 🧊 AES-encrypted password storage
- 📋 Bootstrap-styled UI
- 📊 Security Score page (detect reused passwords)
- ✅ Ready to expand into a full-featured password manager or browser extension

## 🧠 Tech Stack

- Python + Flask
- SQLAlchemy (SQLite database)
- Bootstrap for frontend
- Cryptography (Fernet/AES) for encryption

## 🛠️ Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/your-username/flask-password-manager.git
cd flask-password-manager

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables (optional)
export FLASK_APP=run.py
export FLASK_ENV=development

# 5. Run the app
flask run
