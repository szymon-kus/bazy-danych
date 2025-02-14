from cassandra.cluster import Cluster

# Połączenie z Cassandrą
def get_db():
    cluster = Cluster(['127.0.0.1'])  # Adres serwera Cassandra
    session = cluster.connect()
    session.set_keyspace('shop')
    return session
