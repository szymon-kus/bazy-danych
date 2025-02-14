import csv
import uuid
import random
import string

def generate_random_user(user_id):
    username = f'user{user_id}'  # Nazwa użytkownika w formacie 'user1', 'user2', 'user3' itd.
    email = username + "@example.com"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    user_id = str(uuid.uuid4())
    return [user_id, username, email, password]

def generate_csv(filename, num_users):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['id', 'username', 'email', 'password'])

        for user_id in range(1, num_users + 1):
            writer.writerow(generate_random_user(user_id))

    print(f"{num_users} użytkowników zostało zapisanych do pliku {filename}")


generate_csv('users_data.csv', 100000)
