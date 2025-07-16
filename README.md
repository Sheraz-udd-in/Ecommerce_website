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
