from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from db import get_connection  # ✅ Import from db.py

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/signup", response_class=HTMLResponse)
def get_signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup")
def signup(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    print(f"SIGNUP request - Username: {username}, Email: {email}")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        print(f"SIGNUP failed - Email exists: {email}")
        raise HTTPException(status_code=400, detail="Email already exists")

    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, password)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"SIGNUP success - User created: {email}")
    return RedirectResponse(url="/login", status_code=303)


@app.get("/login", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    print(f"LOGIN attempt - Email: {email}")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        print(f"LOGIN failed - Wrong credentials: {email}")
        raise HTTPException(status_code=400, detail="Invalid credentials")

    print(f"LOGIN success - Welcome {email}")
    return {"message": f"Welcome, {email}!"}



# crunch
# crul
# 