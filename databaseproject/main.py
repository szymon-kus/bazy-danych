import uuid
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from database import get_db
from models import UserCreate, OrderCreate, Order
import crud

app = FastAPI()
crud.init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/users/")
async def get_users(limit: int = 100, offset: int = 0):
    users = sorted(crud.get_all_users(), key=lambda user: user.username) 
    paginated_users = users[offset:offset + limit]
    return [{"id": str(user.id), "username": user.username, "email": user.email} for user in paginated_users]

@app.get("/orders/all")
def get_all_orders(limit: int = 100, offset: int = 0):
    session = get_db()
    query = "SELECT id, username, product, quantity, status, order_date FROM orders"
    rows = session.execute(query)

    orders = []
    for row in rows:
        orders.append({
            "order_id": str(row.id) if row.id else "Brak ID",
            "username": row.username if row.username else "Brak username",
            "product": row.product if row.product else "Brak produktu",
            "quantity": row.quantity if row.quantity else 0,
            "status": row.status if row.status else "Brak statusu",
            "order_date": row.order_date.strftime("%Y-%m-%d %H:%M:%S") if row.order_date else "Brak daty"
        })

    sorted_orders = sorted(orders, key=lambda order: order["username"])  
    paginated_orders = sorted_orders[offset:offset + limit]
    return {"orders": paginated_orders}



@app.get("/orders/{username}", response_class=HTMLResponse)
async def get_orders_by_username(request: Request, username: str):
    query = "SELECT * FROM orders WHERE username = %s ALLOW FILTERING"
    rows = crud.session.execute(query, (username,))
    results = rows.all()

    if not results:
        raise HTTPException(status_code=404, detail="Orders not found")

    return templates.TemplateResponse("orders_user.html", {"request": request, "username": username, "orders": results})

@app.post("/newuser/")
def register_user(user: UserCreate):
    existing_user = crud.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Użytkownik już istnieje")

    new_user = crud.create_user(user.username, user.email, user.password)

    if not new_user:
        raise HTTPException(status_code=500, detail="Błąd przy tworzeniu użytkownika")

    return {
        "message": "Użytkownik zarejestrowany",
        "user": new_user
    }

@app.post("/neworder/")
def create_order(order: Order):
    order_id = crud.create_order(order)
    return {"message": "Zamówienie utworzone i zapisane w bazie oraz CSV", "order_id": str(order_id)}
