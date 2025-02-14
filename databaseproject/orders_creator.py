import csv
import uuid
import random
from datetime import datetime, timedelta

products = ["Laptop", "Smartphone", "Tablet", "Headphones", "Monitor", "Keyboard", "Mouse", "Charger"]

def create_orders_csv(usernames, filename="orders.csv", orders_per_user=random.randint(1, 3)):
    headers = ['id', 'username', 'product', 'quantity', 'status', 'order_date']

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for username in usernames:
            for _ in range(orders_per_user):
                order_id = uuid.uuid4()
                product = random.choice(products)
                quantity = random.randint(1, 5)
                status = random.choice(['pending', 'shipped', 'delivered'])

                order_date = datetime.now() - timedelta(days=random.randint(0, 30))
                order_date_str = order_date.strftime('%Y-%m-%d %H:%M:%S')  # Format daty

                writer.writerow([order_id, username, product, quantity, status, order_date_str])

def get_usernames_from_csv(filename="users_data.csv"):
    usernames = []

    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            usernames.append(row['username'])

    return usernames

if __name__ == "__main__":
    usernames = get_usernames_from_csv("users_data.csv")

    create_orders_csv(usernames, "orders.csv", orders_per_user=3)
    print(f"Stworzono plik 'orders.csv' z {len(usernames) * 3} zamówieniami.")