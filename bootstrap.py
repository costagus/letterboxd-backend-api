import psycopg2

#  >> dados de conexão com o postgreSQL rodando no docker
DB_CONFIG = {
    "dbname": "letterboxd_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def create_table_and_populate():
    # conectando ao bd
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # criando a tabela users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            username VARCHAR(50) NOT NULL UNIQUE,
            bio TEXT,
            avatar_url VARCHAR(255)
            )
    ''')

    # criando a tabela reviews c/ foreign key para users
    # para cada review, o user_id referencia o id do usuário que fez a review
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id SERIAL PRIMARY KEY,
            movie_title VARCHAR(255) NOT NULL,
            rating INT NOT NULL CHECK (rating >= 0 AND rating <= 10),
            content TEXT NOT NULL,
            poster_url VARCHAR(255),
            user_id INT NOT NULL,
            CONSTRAINT fk_reviews_users FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')

    # o constraint significa que se o usuário for deletado, todas as reviews dele também serão deletadas
    # e que garante a integridade referencial entre as tabelas reviews e users

    # populando a tabela users com dados de exemplo
    users_data = []

    for user in users_data:
        cursor.execute('''
            INSERT INTO users (name, username, bio, avatar_url)
            VALUES (%s, %s, %s, %s)
        ''', user)

    # populando a tabela reviews com dados de exemplo
    reviews_data = []

    for review in reviews_data:
        cursor.execute('''
            INSERT INTO reviews (movie_title, rating, content, poster_url, user_id)
            VALUES (%s, %s, %s, %s, %s)
        ''', review)

    # commitando as alterações e fechando a conexão
    conn.commit()
    cursor.close()
    conn.close()
    print('Deu tudo certo, configurado com sucesso!')

if __name__ == "__main__":
    create_table_and_populate()