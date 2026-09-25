import psycopg2

#  >> dados de conexão com o postgreSQL rodando no docker
DB_CONFIG = {
    "dbname": "letterboxd_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

# criar depois daqui a function/script para criar o banco de dados e as tabelas e popular dados
# funcao q conecta o postgreSQL e retorna a conexao
# criar tabela 'users' e 'reviews' com os campos necessarios
# inserir dados de teste na tabela 'users' e 'reviews'
# fazer commit e fechar a conexao
# def create_table_and_populate():

# if __name__ == "__main__":
    # create_table_and_populate()