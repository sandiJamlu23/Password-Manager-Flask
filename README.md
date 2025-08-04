# 🔐 Flask Password Manager

A not so secure and definitelly not so user-friendly password manager built with Flask that allows you to safely store and manage your passwords with AES encryption.

## ✨ Features

- 2️⃣ 2FA Authentication
- 🛡️ AES-encrypted password storage
- 👤 User authentication and registration
- 🔍 Password strength meter with live feedback
- 📊 Security analysis to detect reused passwords
- 🔄 Add, edit, and delete password entries


## 🛠️ Tech Stack

- **Backend**: Python 3.9, Flask
- **Database**: SQLAlchemy with SQLite (postgreSQL for Railway deployment)
- **Security**: 
  - Bcrypt for password hashing
  - Fernet (AES) for password encryption
  - Flask-Login for session management
- **Frontend**: 
  - Bootstrap 5
  - Custom JavaScript for password strength analysis
  - Responsive design

## 📋 Prerequisites

- Python 3.x
- pip (Python package manager)

## 🚀 Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/flask-password-manager.git
cd flask-password-manager
```

2. Create and activate a virtual environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python run.py
```

5. Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
flask-password-manager/
├── app/
│   ├── __init__.py          # App initialization and configuration
│   ├── routes.py            # Route handlers for the application
│   ├── models.py            # Database models for users and password entries
│   ├── crypto.py            # Encryption and decryption logic
│   ├── templates/           # HTML templates for the app
│   │   ├── base.html        # Base template for all pages
│   │   ├── index.html       # Dashboard for saved passwords
│   │   ├── login.html       # Login page
│   │   ├── register.html    # Registration page
│   │   ├── add.html         # Add new password page
│   │   ├── edit.html        # Edit password page
│   │   ├── security.html    # Security analysis page
│   └── static/              # Static files (CSS, JS)
│       ├── style.css        # Custom styles
│       ├── js/
│           ├── darkmode.js  # Dark mode toggle logic
│           ├── passwordStrength.js # Password strength meter logic
├── run.py                   # Entry point for running the app
├── requirements.txt         # Python dependencies
├── README.md                # Project overview and setup instructions
├── Procfile                 # Deployment configuration for Heroku
├── nixpacks.toml            # Nixpacks configuration for deployment
```

## 🔒 Security Features

- AES encryption for stored passwords
- Bcrypt password hashing for user accounts
- Password strength analysis
- Detection of password reuse
- Secure session management
- CSRF protection

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request
6. OR you could use DOCKER 

