<img width="1905" height="763" alt="Screenshot 2026-03-30 205150" src="https://github.com/user-attachments/assets/2517b837-1384-4542-878c-82a3a4ef7929" /># 🏦 NexaBank — Django Banking Application

A full-stack multi-user banking web application built with Django, featuring REST API, token authentication, and a clean dark UI.

## ✨ Features

- **Multi-User Support** — Multiple users can register and manage independent accounts
- **Secure Authentication** — Session-based web auth + Token-based REST API auth
- **Account Management** — Savings and Current account types with unique 12-digit account numbers
- **Deposit & Withdrawal** — Instant balance updates with transaction logging
- **Fund Transfer** — Transfer funds between accounts with username search
- **User Search** — Find any user by username before initiating transfer
- **Transaction History** — Complete log of all transactions with timestamps
- **REST API** — Full DRF-powered API with Token Authentication
- **Admin Panel** — Django admin with user, account, and transaction management
- **Responsive UI** — Clean dark-themed interface built with Bootstrap 5

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Django 6.x |
| REST API | Django REST Framework |
| Authentication | Session Auth + DRF Token Auth |
| Frontend | HTML5, CSS3, Bootstrap 5 |
| Database | SQLite3 |
| Version Control | Git, GitHub |
| API Testing | Thunder Client (VS Code) |

---

## 📁 Project Structure
```
nexabank/
├── nexabank/                   # Project settings & main URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                   # Main banking app
│   ├── templates/
│   │   └── accounts/
│   │       ├── base.html       # Master template
│   │       ├── landing.html    # Home page
│   │       ├── login.html      # Login page
│   │       ├── register.html   # Register page
│   │       └── dashboard.html  # Main dashboard
│   ├── admin.py                # Admin panel config
│   ├── api_views.py            # REST API views
│   ├── models.py               # BankAccount, Transaction models
│   ├── serializers.py          # DRF serializers
│   ├── urls.py                 # URL routing
│   └── views.py                # Web views
├── docs/
│   └── dashboard.png           # Screenshot
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/api/register/` | ❌ | Register new user |
| POST | `/api/login/` | ❌ | Login & get token |
| GET | `/api/account/` | ✅ | Account details |
| GET | `/api/transactions/` | ✅ | Transaction history |
| POST | `/api/deposit/` | ✅ | Deposit amount |
| POST | `/api/withdrawal/` | ✅ | Withdraw amount |
| POST | `/api/transfer/` | ✅ | Transfer to another account |

### API Usage Example

**Register:**
```json
POST /api/register/
{
    "username": "madhav",
    "email": "madhav@gmail.com",
    "password": "test1234",
    "account_type": "savings"
}
```

**Response:**
```json
{
    "message": "Account successfully bana!",
    "token": "9a8b7c6d5e...",
    "username": "madhav",
    "account_number": "123456789012"
}
```

**Authenticated Request:**
```
Headers:
Authorization: Token 9a8b7c6d5e...
```

---

## ⚙️ Local Setup
```bash
# 1. Clone the repository
git clone https://github.com/Madhav-Sharma-2003/nexabank.git
cd nexabank

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create superuser (for admin panel)
python manage.py createsuperuser

# 6. Start server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.
Admin panel: `http://127.0.0.1:8000/admin/`


## 🗃️ Database Models

### BankAccount
| Field | Type | Description |
|-------|------|-------------|
| user | OneToOneField | Linked Django user |
| account_number | CharField | Unique 12-digit number |
| account_type | CharField | Savings / Current |
| balance | DecimalField | Current balance |
| created_at | DateTimeField | Account creation time |

### Transaction
| Field | Type | Description |
|-------|------|-------------|
| account | ForeignKey | Linked bank account |
| transaction_type | CharField | deposit / withdrawal / transfer |
| amount | DecimalField | Transaction amount |
| description | CharField | Optional note |
| timestamp | DateTimeField | Transaction time |

## 🔐 Security Features

- CSRF protection on all web forms
- Password hashing via Django's built-in auth
- Token authentication for REST API
- Login required on all protected views
- Balance validation before transactions
- Duplicate account number prevention

## 🚀 Future Improvements

- [ ] Deploy on Railway / Render
- [ ] JWT Authentication
- [ ] Transaction PDF export
- [ ] Fixed Deposit (FD) feature
- [ ] Email notifications on transactions
- [ ] Pagination for transaction history
