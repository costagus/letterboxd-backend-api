from flask import Flask, jsonify, g
import psycopg2
from models.users import Users

app = Flask(__name__)

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

# agora teremos as rotas da nossa API
# teste p/ ver se o flask tá rodando, e se a conexão com o banco de dados tá funcionando
@app.route('/')
def index():
    return jsonify({"message": "letterboxd rodando!"})   

# endpoint p/ pegar o perfil de um usuário pelo id, incluindo suas reviews
@app.route('/users/<int:user_id>')
def get_user_profile(user_id):
    cursor = get_db().cursor()
    users_model = Users(cursor)
    user_data = users_model.get_by_id(user_id)
    cursor.close()

    if user_data is None:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return jsonify(user_data)

# explicação do que foi feito: criamosuma rota que recebe o id do usuário como parâmetro, e chamamos o método get_by_id da classe Users, 
# que retorna um dicionário com os dados do usuário e suas reviews.. se o usuário não for encontrado, retornamos um erro 404!!

if __name__ == '__main__':
    # porta 3000 igual nos slides da aula
    app.run(host='0.0.0.0', port=3000, debug=True)