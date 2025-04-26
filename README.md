# 🔐 Flask Password Manager

A not so secure and definitelly not so user-friendly password manager built with Flask that allows you to safely store and manage your passwords with AES encryption.

## ✨ Features

- 🛡️ AES-encrypted password storage
- 👤 User authentication and registration
- 🔍 Password strength meter with live feedback
- 📊 Security analysis to detect reused passwords
- 🎨 Clean and responsive Bootstrap UI
- 🔄 Add, edit, and delete password entries
- 📱 Mobile-friendly design

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask
- **Database**: SQLAlchemy with SQLite
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
│   ├── routes.py            # Route handlers
│   ├── models.py            # Database models
│   ├── crypto.py            # Encryption utilities
│   └── templates/           # HTML templates
├── static/
│   ├── style.css           # Custom styles
│   └── js/
│       └── passwordStrength.js  # Password strength checker
├── run.py                  # Application entry point
└── requirements.txt        # Project dependencies
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

## 📄 License

This project is released under the Unlicense - see the [LICENSE](LICENSE) file for details.
