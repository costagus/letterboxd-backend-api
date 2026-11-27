from flask import Flask, jsonify, g
import psycopg2
from models.users import Users
from flask import request, send_from_directory
from models.reviews import Reviews
import logging
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_pydantic import validate
from pydantic_models.schemas import LoginSchema, ReviewCreateSchema

app = Flask(__name__)

# configurando a chave secreta para JWT
app.logger.setLevel(logging.DEBUG) # para ver os logs no console
app.config['JWT_SECRET_KEY'] = 'chaver-super-secreta-letterboxd-utfpr' 
jwt = JWTManager(app) # objeto que valida e cria tokens JWT

# configurando a conexão com o banco de dados
DB_CONFIG = {
    "dbname": "letterboxd_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

# usamos o g do flask p/ armazenar a conexão com o banco de dados, assim não precisamos abrir e fechar a conexão a cada requisição

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(**DB_CONFIG)
    return g.db

# mas precisamos fechar a conexão com o banco de dados no final de cada requisição, então usamos o teardown_appcontext do flask

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# tratamento de erros globais
# retornar erros em JSON para que o frontend possa tratar melhor
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Erro: {e}")
    if isinstance(e, HTTPException): # se for um erro HTTP, retorna o código e a descrição do erro
        return jsonify(error=str(e.description)), e.code
    return jsonify(error='Erro do servidor'), 500 # 500: Internal Server Error (erro genérico do servidor)

# agora teremos as rotas da nossa API
@app.route('/')
@app.route('/app')
def serve_frontend():
    return send_from_directory('static', 'index.html')

# endpoint p/ pegar o perfil de um usuário pelo id, incluindo suas reviews
@app.route('/users/<int:user_id>')
def get_user_profile(user_id):
    if 'text/html' in request.headers.get('Accept', ''):
        return send_from_directory('static', 'index.html')

    cursor = get_db().cursor()
    users_model = Users(cursor)
    user_data = users_model.get_by_id(user_id)
    cursor.close()

    if user_data is None:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return jsonify(user_data)

# explicação do que foi feito: criamosuma rota que recebe o id do usuário como parâmetro, e chamamos o método get_by_id da classe Users, 
# que retorna um dicionário com os dados do usuário e suas reviews.. se o usuário não for encontrado, retornamos um erro 404!!

#rota de reviews p buscar avaliações
@app.route('/reviews', methods=['GET'])
def get_reviews():
    if 'text/html' in request.headers.get('Accept', ''):
        return send_from_directory('static', 'index.html')
    termo = request.args.get('termo') or request.args.get('q') or '' #pega o texto digitado, se não tiver nada usa vazio
    page = request.args.get('page', default=1, type=int) #pega o num de pag q queremos buscar,se ñ informar usa 1
    limit = request.args.get('limit', default=10, type=int) #define resultado por pagina
#acesso ao banco
    cursor = get_db().cursor()
    reviews_model = Reviews(cursor)
    results = reviews_model.search(query=termo, page=page, limit=limit)
    cursor.close()
#devolve o banco em jsonify
    return jsonify({
        "page": page,
        "limit": limit,
        "termo_buscado": termo,
        "total_results": len(results),
        "results": results
    })

# rota parametrizada de reviews p buscar avaliações por termo na url
@app.route('/reviews/search/<string:termo>', methods=['GET'])
def get_reviews_by_term(termo):
    cursor = get_db().cursor()
    reviews_model = Reviews(cursor)
    results = reviews_model.search(query=termo, page=1, limit=10)
    cursor.close()
    return jsonify({
        "termo_buscado": termo,
        "total_results": len(results),
        "results": results
    })

# recup: rota p/ buscar usuários com paginação

@app.route('/users', methods=['GET'])
def get_users():
    termo = request.args.get('termo') or request.args.get('q') or ''
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=5, type=int)

    cursor = get_db().cursor()
    users_model = Users(cursor)
    results = users_model.search(query=termo, page=page, limit=limit)
    cursor.close()

    return jsonify({
        "page": page,
        "limit": limit,
        "termo_buscado": termo,
        "total_results": len(results),
        "results": results
    }), 200

# projeto 2 - rotas de login e inserção (REST)

# rota de login (bcrypt p/ validação de senha e JWT p/ autenticação)
@app.route('/login', methods=['POST'])
@validate() # validação do schema pydantic
def login(body: LoginSchema): # 'body:' é o corpo da req
    cursor = get_db().cursor()
    users_model = Users(cursor)
    user = users_model.login(body.username, body.password)
    cursor.close()

    if not user:
        return jsonify({"error": "Usuário ou senha incorretos"}), 401

    # gerando token JWT
    token = create_access_token(
        identity=str(user['id']), # id do usuário como identidade
        additional_claims={"username": user['username']} # informações adicionais no token (opcional)
    )
    app.logger.debug(f"Usuário {user['username']} logado com sucesso. Token JWT gerado: {token}")
    return jsonify({"message": "Login bem-sucedido", "token": token, "user": user}), 200

# rota de criação de review (POST /reviews) com validação e sanitização dos campos
@app.route('/reviews', methods=['POST'])
@jwt_required() # rota protegida, precisa de token JWT válido
@validate() # validação do schema pydantic
def create_review(body: ReviewCreateSchema): 
    # extrai id do usuário do token JWT
    user_id = int(get_jwt_identity())
    claims = get_jwt() # pega os claims do token JWT (claims = informações adicionais)

    db = get_db()
    cursor = db.cursor()
    reviews_model = Reviews(cursor)

    new_id = reviews_model.create(
        movie_title=body.movie_title,
        rating=body.rating,
        content=body.content,
        poster_url=body.poster_url,
        user_id=user_id
    )
    # body é o corpo da requisição, que já foi validado e sanitizado pelo schema pydantic
    # gravando a nova review no banco de dados
    db.commit() # salvando no bd
    cursor.close()

    app.logger.info(f"Nova review criada pelo usuário {claims['username']} (ID: {user_id}): {body.movie_title} - Nota: {body.rating}")
    # retorna status 201 (Created) e o id da nova review
    return jsonify({"message": "Review criada com sucesso", "review_id": new_id}), 201

if __name__ == '__main__':
    # porta 3000 igual nos slides da aula
    app.run(host='0.0.0.0', port=3000, debug=True)