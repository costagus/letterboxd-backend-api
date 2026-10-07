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