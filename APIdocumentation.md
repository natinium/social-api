Here’s how to update the **Markdown documentation** to include the registration (signup) API, based on the request and response structure you provided.

---

# **2. How to Use the Authentication API**

A list of the api endpoints could be found at http://127.0.0.1:8000/swagger or http://127.0.0.1:8000/redoc

### **2.1. Register (Signup) API**

To create a new user, send a POST request to the `/api/users/register/` endpoint with the user's email, username, and password.

#### Request

- **URL**: `POST http://127.0.0.1:8000/api/users/register/`
- **Body** (JSON):
  ```json
  {
      "email": "user200@example.com",
      "username": "username200",
      "password": "password123",
      "password2": "password123"
  }
  ```

In this example:
- `password` and `password2` should match for successful registration.

#### Example with cURL

```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ -H "Content-Type: application/json" -d '{"email": "user200@example.com", "username": "username200", "password": "password123", "password2": "password123"}'
```

#### Response

You will receive a response like this:

```json
{
    "token": "9da8dd5d9e8a1c2d2fae3f31f81942841893a12e",
    "user_id": 4,
    "email": "user200@example.com",
    "username": "username200"
}
```

Here:
- `token` is the authentication token that will be used for subsequent requests.
- `user_id`, `email`, and `username` are the details of the registered user.

---

### **2.2. Login API**

Once registered, you can use the **Login** API to obtain an access token for authenticated requests.

#### Request

- **URL**: `POST http://127.0.0.1:8000/api/users/login/`
- **Body** (JSON):
  ```json
  {
      "username": "username200",
      "password": "password123"
  }
  ```

#### Example with cURL

```bash
curl -X POST http://127.0.0.1:8000/api/users/login/ -H "Content-Type: application/json" -d '{"username": "username200", "password": "password123"}'
```

#### Response

You will receive a response like this:

```json
{
    "token": "9da8dd5d9e8a1c2d2fae3f31f81942841893a12e",
    "user_id": 4,
    "email": "user200@example.com",
    "username": "username200"
}
```

Here, the `token` field represents the authentication token that will be used for further requests.

---

### **2.3. Use Token for Protected Endpoints**

Once you have the token, you can use it to authenticate requests to protected endpoints. Include the token in the `Authorization` header as a Bearer token.

#### Request

- **URL**: `GET http://127.0.0.1:8000/protected/`
- **Headers**:
  ```
  Authorization: Bearer 9da8dd5d9e8a1c2d2fae3f31f81942841893a12e
  ```

#### Example with cURL

```bash
curl -X GET http://127.0.0.1:8000/protected/ -H "Authorization: Bearer 9da8dd5d9e8a1c2d2fae3f31f81942841893a12e"
```

#### Response

If the token is valid, you will receive a successful response from the protected endpoint.

---

## **3. Conclusion**

By using **Token Authentication**, we provide secure access to protected endpoints. You can:

- **Register** a new user at `/api/users/register/` by providing `email`, `username`, and `password`.
- **Login** with the registered user credentials to get a `token` at `/api/users/login/`.
- Use the `token` to authenticate requests to protected endpoints by including it in the `Authorization` header.

For testing, you can use **Postman**, **cURL**, or any HTTP client. The `token` will be used in subsequent requests to authenticate the user.