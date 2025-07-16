
# 🛒 Django E-commerce API

This project is a RESTful e-commerce backend built with **Django** and **Django REST Framework**. It features role-based authentication, JWT support, cart and order management, and vendor-customer interaction.

---

## 🔧 Features

- User registration with roles (`customer`, `vendor`)
- JWT-based authentication (`rest_framework_simplejwt`)
- Product listing, filtering, and creation (vendor only)
- Add to cart / remove from cart / view cart
- Cart-based order creation (purchase)
- Vendor order management with order status control
- Caching and pagination support

---

## 📦 Tech Stack

- **Backend:** Django, Django REST Framework
- **Auth:** JWT (via SimpleJWT)
- **Database:** SQLite (default, can be swapped)
- **Cache:** In-memory (Django cache framework)
- **API Testing:** Postman

---

## 🚀 API Endpoints

### 🔐 Authentication

| Method | Endpoint         | Description               |
|--------|------------------|---------------------------|
| POST   | `/register/`     | Register new user         |
| POST   | `/token/`        | Get JWT token             |
| POST   | `/token/refresh/`| Refresh JWT token         |

---

### 📦 Product Management

| Method | Endpoint                    | Access     | Description           |
|--------|-----------------------------|------------|-----------------------|
| GET    | `/products/`                | Auth       | List & filter products|
| GET    | `/products/<id>/`           | Auth       | Get product detail    |
| POST   | `/products/create/`         | Vendor     | Create new product    |
| PUT/PATCH/DELETE | `/products/update/<id>/` | Vendor | Modify/Delete product |

---

### 🛒 Cart

| Method | Endpoint             | Description                       |
|--------|----------------------|-----------------------------------|
| GET    | `/cart/`             | View cart summary                 |
| POST   | `/cart/<product_id>/`| Add product to cart               |
| DELETE | `/cart/<product_id>/`| Remove product from cart          |

---

### 📦 Orders

| Method | Endpoint               | Description                       |
|--------|------------------------|-----------------------------------|
| GET    | `/purchase/`           | Convert cart to orders (customer) |
| GET    | `/orders/`             | View vendor orders                |
| GET    | `/orders/<id>/`        | View specific order               |
| PATCH  | `/orders/<id>/`        | Update order status (vendor)      |

---

## 🧪 Testing via Postman

1. **Register** a user (customer or vendor).
2. **Obtain token** via `/token/`.
3. Use the **access token** in Bearer Auth for all protected requests.
4. **Try creating products** (if vendor).
5. Add items to cart and simulate a **purchase**.
6. Use the `/orders/` endpoint to view/manage orders (vendor only).

---

## 🗂 Folder Structure
```
ecommerce/
├── app1/
│ ├── views.py
│ ├── models.py
│ ├── serializers.py
│ ├── permissions.py
│ └── urls.py
├── manage.py
└── ...
```
---
# ✅ STEP 1: Start the Server
Make sure your Django server is running:
```
python manage.py runserver
```

# ✅ STEP 2: Register a User
Endpoint: POST /register/
URL: http://127.0.0.1:8000/register/
Body (JSON):

```json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```
# ✅ STEP 3: Get JWT Token
Endpoint: POST /token/
URL: http://127.0.0.1:8000/token/
Body (JSON):

```json
{
  "username": "testuser",
  "password": "password123"
}
```
📌 Save the access token from the response. You’ll use this to authenticate protected endpoints.

# ✅ STEP 4: Set Authorization in Postman
In any request that requires authentication:

Go to the Authorization tab.

Choose Bearer Token.

Paste the access token from Step 3.

# ✅ STEP 5: Test Product Endpoints
🔹 GET /products/
URL: http://127.0.0.1:8000/products/
No body needed. You’ll get a list of products (if any exist).

🔹 POST /products/create/ (Vendor only)
Use a vendor account for this.

URL: http://127.0.0.1:8000/products/create/
Body (JSON):

```json
{
  "name": "iPhone 15",
  "des": "Latest Apple phone",
  "price": 99999,
  "quantity": 10
}
```
🔹 GET /products/<id>/
URL: http://127.0.0.1:8000/products/1/

🔹 PUT /products/update/<id>/ or PATCH
URL: http://127.0.0.1:8000/products/update/1/
Body (JSON):

```json
{
  "price": 89999
}
```
# ✅ STEP 6: Test Cart
🔹 Add to Cart (POST /cart/<product_id>/?quantity=2)
URL: http://127.0.0.1:8000/cart/1/?quantity=2

🔹 View Cart (GET /cart/)
URL: http://127.0.0.1:8000/cart/

🔹 Remove from Cart (DELETE /cart/<product_id>/)
URL: http://127.0.0.1:8000/cart/1/

# ✅ STEP 7: Purchase Items
URL: http://127.0.0.1:8000/purchase/
Method: GET
Creates orders from your cart.

# ✅ STEP 8: View Orders (Vendor)
URL: http://127.0.0.1:8000/orders/
You can also filter:

```arduino
http://127.0.0.1:8000/orders/?status=pending
```

# ✅ STEP 9: Order Detail
🔹 GET /orders/<id>/
URL: http://127.0.0.1:8000/orders/1/

🔹 PATCH /orders/<id>/
URL: http://127.0.0.1:8000/orders/1/
Body:

```json

{
  "status": "shipped"
}
```
🔒 Notes:
Make sure you're using the right token: customer tokens can't create products or view vendor-only pages.

You may need to create a vendor user manually via Django admin or shell.

✅ Optional: Create Vendor via Shell
```bash

python manage.py shell
```
```python

from django.contrib.auth import get_user_model
User = get_user_model()
vendor = User.objects.create_user(username='vendor1', password='pass123', role='vendor')
```
