import csv
import os
import uuid
from datetime import datetime

from cassandra.cluster import Cluster
from cassandra.cqlengine.connection import get_session, setup
from passlib.context import CryptContext
from database import get_db

session = get_db()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

CSV_FILE = "users_data.csv"

def init_db():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.set_keyspace('shop')  # Ustawienie keyspace globalnie
    setup(['127.0.0.1'], "shop")  # Ustawienie połączenia dla cqlengine

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def save_user_to_csv(user_id: str, username: str, email: str):
    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["id", "username", "email"])  # Nagłówki

        writer.writerow([user_id, username, email])


def create_user(username: str, email: str, password: str):
    try:
        session.set_keyspace('shop')

        user_id = uuid.uuid4()
        hashed_password = hash_password(password)

        query = "INSERT INTO users (id, username, email, password) VALUES (%s, %s, %s, %s)"
        session.execute(query, (user_id, username, email, hashed_password))

        save_user_to_csv(str(user_id), username, email)

        return {"id": str(user_id), "username": username, "email": email}

    except Exception as e:
        print(f"Błąd w create_user: {e}")
        raise

def get_all_users():
    query = "SELECT id, username, email FROM users"
    rows = session.execute(query)
    return rows

def create_order(order):
    query = "INSERT INTO orders (id, username, product, quantity, status, order_date) VALUES (%s, %s, %s, %s, %s, %s)"
    session.execute(query, (order.id, order.username, order.product, order.quantity, order.status, order.order_date))
    save_order_to_csv(order)


def save_order_to_csv(order):
    file_exists = os.path.isfile("orders.csv")

    with open("orders.csv", mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["id", "username", "product", "quantity", "status", "order_date"])

        writer.writerow([order.id, order.username, order.product, order.quantity, order.status, order.order_date])

def get_orders(username: str):
    session = get_session()
    query = f"SELECT * FROM shop.orders WHERE username = '{username}'"
    print("QUERY:", query)
    result = session.execute(query)
    orders = list(result)
    print("RESULT:", orders)
    return orders


def get_all_orders():
    session = get_session()
    rows = session.execute("SELECT * FROM shop.orders")
    orders = [dict(row) for row in rows]
    return orders


