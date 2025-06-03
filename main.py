from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from db import get_connection

from passlib.context import CryptContext

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
def get_signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
def signup(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    conn = get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already exists")

        hashed_password = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    return RedirectResponse(url="/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()

        if not result or not verify_password(password, result[0]):
            raise HTTPException(status_code=400, detail="Invalid credentials")

    finally:
        cursor.close()
        conn.close()

    return {"message": f"Welcome, {email}!"}
