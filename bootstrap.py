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

    # comando p limpar a tabela antes de reinserior os dados (limpa e zera ids)
    cursor.execute("TRUNCATE TABLE reviews, users RESTART IDENTITY CASCADE;")

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
    users_data = [
        ("Gustavo Melo", "gustavomelo", "Cinefilo e estudante da UTFPR.", "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150"),
        ("Veronica", "vero", "Aprecio terror psicologico e cinema cult.", "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150"),
        ("Pedro", "pedrothebest", "Fã de blockbusters e super-herois.", "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=150"),
        ("Inacio", "lula13", "Critico casual de filmes de suspense e drama.", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150"),
        ("Luna", "lunaurora", "Amante de animacoes e musicais artisticos.", "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150"),
        ("Erika", "erikahilt", "Viciada em plot twists e thrillers sombrios.", "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150")
    ]

    for user in users_data:
        cursor.execute('''
            INSERT INTO users (name, username, bio, avatar_url)
            VALUES (%s, %s, %s, %s)
        ''', user)

    # populando a tabela reviews com dados de exemplo
    reviews_data = [
        # gustavo (user_id: 1)
        ("Pulp Fiction", 5, "Classico absoluto do Tarantino. Dialogos e trilha sonora brilhantes!", "https://image.tmdb.org/t/p/original/x1QZHSq9AzreIVbsp8VgYemAjV0.jpg", 1),
        ("Parasite", 5, "Uma critica social genial em formato de suspense impecavel.", "https://image.tmdb.org/t/p/original/nCgxk9XgBiavhPdn7AjzJLVsDLr.jpg", 1),
        # veronica (user_id: 2)
        ("Possession", 5, "Atuacao perturbadora da Isabelle Adjani. Um dos terrores psicologicos mais viscerais ja feitos.", "https://image.tmdb.org/t/p/original/A9bnRn05riOKWftvQlLKa2gl51n.jpg", 2),
        ("Mulholland Drive", 5, "Lynch em seu auge. Um pesadelo hipnotizante e misterioso.", "https://image.tmdb.org/t/p/original/frjC0WxpPNxGUP4a7FrXdXlXQZo.jpg", 2),
        # pedro (user_id: 3)
        ("Spider Man Brand New Day", 4, "A expectativa ta enorme pra essa nova fase do Aranha nos cinemas!", "https://image.tmdb.org/t/p/original/tV712n7bMaRuaKyltFl65HPNRiP.jpg", 3),
        ("Avengers Doomsday", 4, "Robert Downey Jr de volta como Doutor Destino vai ser epico.", "https://image.tmdb.org/t/p/original/cWXtJhrlruF8CeYuaBGE8vdj3Q9.jpg", 3),
        # inacio (user_id: 4)
        ("Blair Witch", 4, "O pioneiro do found footage. Simples, cru e incrivelmente tenso.", "https://image.tmdb.org/t/p/original/mGRrIt7CEj9l5TMixr5p42GNbcr.jpg", 4),
        ("Resident Evil", 4, "Divertido como acao zumbi, mesmo fugindo um pouco dos jogos.", "https://image.tmdb.org/t/p/original/sLa3Lhy61GNrFlguN8zHBNUGbvN.jpg", 4),
        # luna (user_id: 5)
        ("Coraline", 5, "Animacao stop-motion visualmente linda e assustadoramente tocante.", "https://image.tmdb.org/t/p/original/5wwIi8Jdr3nzGCJ9pjaSnRf09k8.jpg", 5),
        ("La La Land", 5, "Cores, fotografia e musica apaixonantes. Final agridoce e realista.", "https://image.tmdb.org/t/p/original/6JweOZD2iXxjE6GBPtsujtDgW6i.jpg", 5),
        # erika (user_id: 6)
        ("Gone Girl", 5, "Rosamund Pike perfeita. Um dos melhores thrillers psicologicos do Fincher.", "https://image.tmdb.org/t/p/original/gZsNeosjq3DZAJunrd65KMsmlYJ.jpg", 6),
        ("Supergirl", 4, "Ansiosa pela adaptacao de Woman of Tomorrow, a historia dos quadrinhos eh fantastica!", "https://image.tmdb.org/t/p/original/uhzRnTW4DM13UQBvZP3eVNzQTuz.jpg", 6)
    ]

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