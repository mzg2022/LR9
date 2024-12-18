from fastapi import FastAPI, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.auth import create_access_token, verify_password, verify_token
from app.db import init_db, SessionLocal
from app.middleware import JWTMiddleware
from app.models import User
from app.schemas import TransactionOut, UserCreate, TransactionCreate, TopUpRequest
from app.crud import create_user, get_user_by_username, create_transaction, get_transactions_by_user

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

app.add_middleware(
    JWTMiddleware,
    excluded_paths=["/", "/static", "/login", "/register"]
)


# Функция для текущего пользователя
def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = verify_token(token)
        return payload.get("sub")
    except:
        return None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    user_authenticated = get_current_user(request) is not None
    return templates.TemplateResponse("index.html", {"request": request, "user_authenticated": user_authenticated})

@app.get("/logout")
async def logout(request: Request):
    response = JSONResponse({"message": "Logged out"})
    response.delete_cookie("access_token")
    return response

@app.post("/api/top-up")
async def top_up_balance(
    top_up_data: TopUpRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    username = get_current_user(request)
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if top_up_data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    user.balance += top_up_data.amount
    db.commit()

    return {"new_balance": user.balance}


@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    user_authenticated = get_current_user(request) is not None
    return templates.TemplateResponse("register.html", {"request": request, "user_authenticated": user_authenticated})


@app.post("/api/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    create_user(db, user)
    return JSONResponse({"message": "User registered successfully"}, status_code=201)

@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    user_authenticated = get_current_user(request) is not None
    return templates.TemplateResponse("login.html", {"request": request, "user_authenticated": user_authenticated})


@app.post("/api/login")
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username})
    response = JSONResponse({"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=3600
    )
    return response


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    username = get_current_user(request)
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transactions = get_transactions_by_user(db, user.id)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "transactions": transactions,
    })


@app.post("/api/transactions", response_model=TransactionOut)
async def create_transaction_api(
    request: Request,
    transaction_data: TransactionCreate,  # Получаем данные в JSON
    db: Session = Depends(get_db),
):
    username = get_current_user(request)
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.balance < transaction_data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    receiver = get_user_by_username(db, transaction_data.receiver_username)
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    transaction = create_transaction(
        db,
        {
            "sender_id": user.id,
            "receiver_id": receiver.id,
            "amount": transaction_data.amount,
            "description": transaction_data.description,
        },
    )
    return transaction

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)


