class Reviews:
    # trabalhar as avaliacoes
    def __init__(self, cursor=None):
        # recebe e guarda o acesso ao banco
        self._cursor = cursor

    # funcao para pesquisar as avaliacoes
    def search(self, query='', page=1, limit=10):
        # se nao tiver acesso ao banco, nao faz a pesquisa
        if not self._cursor:
            return []

        try:
            # define a pagina atual
            page = max(1, int(page))
            # define quantos resultados aparecem por pagina
            limit = max(1, int(limit))
        # se der algum erro, volta para os valores padrao
        except (ValueError, TypeError):
            page = 1
            limit = 10

        # calcula de onde a busca deve comecar
        offset = (page - 1) * limit

        search_pattern = f"%{query}%"

        # monta a consulta para buscar os dados no banco
        sql = """
            SELECT 
                r.id,
                r.movie_title,
                r.rating,
                r.content,
                r.poster_url,
                r.user_id,
                u.name AS user_name,
                u.username AS user_username
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            WHERE r.movie_title ILIKE %s
            ORDER BY r.id DESC
            LIMIT %s OFFSET %s;
        """

        # executa a consulta usando os valores da pesquisa
        self._cursor.execute(sql, (search_pattern, limit, offset))

        # pega os resultados encontrados
        rows = self._cursor.fetchall()

        # cria uma lista para guardar os resultados
        results = []

        # passa por cada resultado encontrado
        for row in rows:
            # organiza cada resultado em formato de dicionario
            results.append({
                "id": row[0],
                "movie_title": row[1],
                "rating": row[2],
                "content": row[3],
                "poster_url": row[4],
                "user_id": row[5],
                "user_name": row[6],
                "user_username": row[7]
            })

        return results