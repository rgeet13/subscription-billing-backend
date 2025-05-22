# Django Subscription Billing Backend

This is a Django-based subscription billing backend that supports:

- User sign-up and login with JWT authentication
- Plan subscription and unsubscription
- Automatic monthly invoice generation using Celery
- Invoice payment tracking
- Overdue invoice detection and reminders
- Mock payment for invoices
- Swagger (OpenAPI) documentation

---

## 🚀 Features

### Authentication
- User registration and login
- JWT-based auth (`access`, `refresh` tokens)

### Plans and Subscriptions
- Predefined Plans: Basic, Pro, Enterprise
- Users can subscribe/unsubscribe
- Subscription fields: `start_date`, `end_date`, `status`

### Invoices
- Generated automatically by Celery for active subscriptions
- Fields: `user`, `plan`, `amount`, `issue_date`, `due_date`, `status`
- Mark overdue if unpaid after due date
- Manual (mock) payment supported

### Celery Integration
- `generate_invoices` – creates invoices daily for subscriptions starting today
- `mark_overdue_invoices` – marks invoices as overdue if due
- `send_payment_reminders` – console prints reminder for unpaid invoices

### API Endpoints
- `/api/accounts/register/` – Register
- `/api/accounts/login/` – Login
- `/api/token/refresh/` – JWT refresh
- `/api/billing/subscribe/` – Subscribe to a plan
- `/api/billing/unsubscribe/` – Cancel subscription
- `/api/billing/invoices/` – List invoices (GET)
- `/api/billing/invoices/<id>/` – Invoice details (GET)
- `/api/billing/invoices/<uuid:invoice_id>/pay/` – Pay invoice (POST)

---

## 🔧 Setup

### 1. Clone & Install

```bash
git clone https://github.com/rgeet13/subscription-billing-backend
cd billing_project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Redis (Required for Celery)
```bash
# Linux/macOS
redis-server

# Windows (use Redis from WSL or Docker)
```

### 3. Apply Migrations & Create Superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Start Services
```bash
# Run Django server
python manage.py runserver

# Run Celery worker
celery -A billing_project worker --loglevel=info

# Run Celery beat (for periodic tasks)
celery -A billing_project beat --loglevel=info
```

### 5. Swagger (OpenAPI)
- Visit `http://127.0.0.1:8000/swagger/` for API documentation

---

## 📝 Future Enhancements
[ ] - Stripe integration for real payments
[ ] - Email sending (not just console)
[ ] - Admin interface for invoice management
[ ] - Better invoice filtering and pagination
