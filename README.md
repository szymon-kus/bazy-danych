## Krótki opis
Projekt to aplikacja internetowa oparta na frameworku FastAPI, umożliwiająca zarządzanie użytkownikami oraz zamówieniami. 
Aplikacja korzysta z bazy danych Cassandra oraz obsługuje operacje CRUD na użytkownikach i zamówieniach. Możliwe jest wyświetlanie zamówień i użytkowników, a także dodawanie nowych.



### Uruchomienie
- importy (pip install fastapi uvicorn cassandra-driver passlib bcrypt pydantic jinja2)
- Struktura tabel -

---- CREATE TABLE IF NOT EXISTS orders (
        ...     id UUID PRIMARY KEY,
        ...     username TEXT,
        ...     product TEXT,
        ...     quantity INT,
        ...     status TEXT,
        ...     order_date TIMESTAMP
        ... );
        
--- CREATE TABLE IF NOT EXISTS users (id UUID PRIMARY KEY,
        ...     username TEXT,
        ...     email TEXT,
        ...     password TEXT
        ... );

- uruchomienie plików csvcreator.py i order_creator.py (jeśli chcemy wygenerować nowy zestaw danych)
- skopiowanie danych z plików csv do cassandry (COPY shop.users (id, username, email, password) FROM 'users_data.csv' WITH HEADER = TRUE;      COPY shop.orders (id, username, product, quantity, status, order_date) FROM 'orders.csv' WITH HEADER = TRUE;
- uruchomienie projektu



Możliwe jest dodawanie użytkownik i zamówień (przez POSTMAN w następującym formacie:

zamówienia:
{
  "username": "jan_kowalski",
  "product": "Laptop Lenovo",
  "quantity": 1,
  "status": "W realizacji"
}


użytkownicy:
{
  "username": "janek",
  "email": "jan@example.com",
  "password": "super_tajne_haslo"
}



## Baza danych 
Aplikacja korzysta z połączenia z Cassandrą
from cassandra.cluster import Cluster

def get_db():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.set_keyspace('shop')
    return session

    
## ODczyt danych 
Aplikacja zapisuje użytkowników oraz zamówienia w plikach CSV, które tworzą się poprzez uruchomienie plików csvcreator.py i orderscreator.py (pliki te generują 
określoną ilość losowych rekordów)


Projekt umożliwia zarządzanie użytkownikami oraz zamówieniami za pomocą API opartego na FastAPI i bazie danych Cassandra. 
Obsługuje operacje CRUD, sortowanie i zapis danych do plików CSV. 
Aplikacja renderuje również stronę główną oraz zamówienia użytkownika za pomocą Jinja2.
