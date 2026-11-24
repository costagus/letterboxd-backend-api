import bcrypt

class Users:
    def __init__(self, cursor):
        self._cursor = cursor

    def get_by_id(self, user_id):
        self._cursor.execute('''
        SELECT id, name, username, bio, avatar_url 
        FROM users 
        WHERE id = %s
        ''', (user_id,))

        # o user_id é passado como uma tupla (user_id,) para evitar SQL injection

        # user_row é uma tupla com os dados do usuári ou None se não existir

        user_row = self._cursor.fetchone()
        if not user_row:
            return None

        self._cursor.execute('''
            SELECT id, movie_title, rating, content, poster_url
            FROM reviews 
            WHERE user_id = %s
            ''', (user_id,))

        reviews_rows = self._cursor.fetchall()

        # lista de dicionários representando as reviews do usuário
        reviews = [
            {
                "id": review[0],
                "movie_title": review[1],
                "rating": review[2],
                "content": review[3],
                "poster_url": review[4]
            }
            for review in reviews_rows
        ]

        # pega os dados do usuário e as reviews dele e monta um dicionário com tudo isso usando
        # compreensão de listas para as reviewse dps retorna esse dicionário representando o usuário e suas reviews

        return {
            "id": user_row[0],
            "name": user_row[1],
            "username": user_row[2],
            "bio": user_row[3],
            "avatar_url": user_row[4],
            "reviews": reviews
        }

    # recup: fazendo paginação para usuários, com busca por termo, limitando resultados e pulando páginas anteriores
    
    def search(self, query='', page=1, limit=5):
        # definir página e limite, o try p/ garantir que sejam inteiros positivos, se não forem, usa o padrão 1 e 5
        try:
            page = max(1, int(page))
            limit = max(1, int(limit))
        except (ValueError, TypeError):
            page = 1
            limit = 5
        # offset para pular os resultados das páginas anteriores, e search_pattern para buscar o termo com ILIKE
        offset = (page - 1) * limit
        search_pattern = f"%{query}%"
        # query
        self._cursor.execute("""
            SELECT id, name, username, bio, avatar_url
            FROM users
            WHERE name ILIKE %s OR username ILIKE %s
            ORDER BY id ASC 
            LIMIT %s OFFSET %s;
        """, (search_pattern, search_pattern, limit, offset)) # evitando SQL injection
        rows = self._cursor.fetchall()
        return [
            {
                "id": row[0],
                "name": row[1],
                "username": row[2],
                "bio": row[3],
                "avatar_url": row[4]
            }
            for row in rows
        ]

    def login(self, username, password):
        self._cursor.execute('''
            SELECT id, name, username, bio, avatar_url, password
            FROM users
            WHERE username = %s
        ''', (username,))
        user_row = self._cursor.fetchone()

        # se o usuário não for encontrado, retorna None
        if not user_row:
            return None

        # user_row[5] é a senha hash armazenada no banco de dados
        stored_password_hash = user_row[5]
        # transforma a senha digitada e o hash do banco em bytes e comparamos
        senha_bateu = bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8'))

        if senha_bateu:
            # retorna um dicionário com os dados do usuário, sem a senha, se a senha estiver correta
            return {
                "id": user_row[0],
                "name": user_row[1],
                "username": user_row[2]
            }
        return None