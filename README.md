# Multi-Tenant SaaS Backend with Django  

A **secure and scalable multi-tenant SaaS backend** built with Django and Django REST Framework (DRF). This project provides **tenant isolation, role-based access control (RBAC), JWT authentication, rate limiting, and audit logs** for a SaaS application.  

## 🚀 Features  
- **Multi-Tenant Support**: Each tenant (organization) has its own isolated data.  
- **Role-Based Access Control (RBAC)**: Roles like `tenant_admin`, `manager`, and `user` control permissions.  
- **JWT Authentication**: Secure login with access and refresh tokens.  
- **Tenant-Aware CRUD**: Users can only access data belonging to their tenant.  
- **Rate Limiting**: Prevents abuse by limiting requests per tenant.  
- **Audit Logs**: Tracks important changes for security and monitoring.  

---

## 🛠️ Setup & Installation  

### **1⃣ Install Dependencies**  
Ensure you have Python 3.9+ and virtualenv installed.  

```bash
# Create a virtual environment
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install django djangorestframework djangorestframework-simplejwt django-redis
```

---

### **2⃣ Start the Django Project**  
```bash
django-admin startproject mysaasproject
cd mysaasproject
python manage.py startapp core
```
Add `core` and `rest_framework` to `INSTALLED_APPS` in `mysaasproject/settings.py`:  

```python
INSTALLED_APPS = [
    ...,
    'rest_framework',
    'core',
]
```

---

### **3⃣ Apply Migrations & Create Superuser**  
```bash
python manage.py makemigrations  
python manage.py migrate  
python manage.py createsuperuser  
```
Follow the prompts to create a superuser for admin access.

---

### **4⃣ Run the Server**  
```bash
python manage.py runserver  
```
API will be available at **http://127.0.0.1:8000/api/**.  

---

## 🔑 Authentication (JWT)  
Use **JWT tokens** to authenticate users.

### **1⃣ Get a Token**  
Send a POST request to:  
```
POST /api/token/
```
With JSON body:  
```json
{
  "username": "admin",
  "password": "yourpassword"
}
```
Response:  
```json
{
  "refresh": "your_refresh_token",
  "access": "your_access_token"
}
```

### **2⃣ Use Token in Requests**  
Include the `Authorization` header in API requests:  
```bash
Authorization: Bearer your_access_token
```

### **3⃣ Refresh Token**  
Send a POST request to:
```
POST /api/token/refresh/
```
With JSON body:  
```json
{
  "refresh": "your_refresh_token"
}
```

---

## 📌 API Endpoints  

| Endpoint                | Method | Description |
|-------------------------|--------|-------------|
| `/api/token/`           | POST   | Get JWT token |
| `/api/token/refresh/`   | POST   | Refresh token |
| `/api/create-tenant/`   | POST   | Create a new tenant |
| `/api/projects/`        | GET    | List all projects (tenant-specific) |
| `/api/projects/`        | POST   | Create a new project |
| `/api/tasks/`           | GET    | List all tasks (tenant-specific) |
| `/api/tasks/`           | POST   | Create a new task |

---

## 🔐 Role-Based Access Control (RBAC)  
User roles determine what actions they can perform:  

| Role         | Permissions |
|-------------|------------|
| `tenant_admin` | Can create projects, manage users, and view tasks. |
| `manager`      | Can manage projects and tasks within a tenant. |
| `user`         | Can view tasks assigned to them. |

---

## ⚡ Multi-Tenant Rate Limiting  
Each tenant has a request limit to prevent API abuse. Default rate:  
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'core.throttles.TenantRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'tenant': '5/minute',
    },
}
```

---

## 📜 Audit Logs (Tracking Changes)  
Every major action (creating/updating a project, task, or user) is **logged automatically**.  

Example log:  
```json
{
    "user": "admin",
    "tenant": "CompanyA",
    "action": "Project created",
    "timestamp": "2025-03-28T12:00:00Z"
}
```



## 📢 Contributing  
Want to improve this project? Contributions are welcome! Fork the repo and submit a pull request.  

---

## 📚 License  
MIT License. Free to use and modify.  

---

## ✨ Author  
Developed by **Lovely Gupta**, a software engineer specializing in Django and SaaS development.

