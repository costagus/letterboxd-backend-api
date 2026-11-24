import bleach # evitar ataques de XSS (Cross-Site Scripting) ao limpar o conteúdo HTML enviado pelo usuário
from pydantic import BaseModel, field_validator # criar modelo de dados e validar/sanitizar os campos

# molde p/ validar dados de login (POST /login)
class LoginSchema(BaseModel):
    username: str
    password: str

# molde p/ validar e limpar a criação de uma review (POST /reviews)
class ReviewCreateSchema(BaseModel):
    movie_title: str
    rating: int
    content: str
    poster_url: str = ''

    # validação e sanitização dos campos de texto para evitar ataques de XSS
    @field_validator('movie_title', 'content', 'poster_url') 
    @classmethod # pertence à classe 
    def sanitizar_texto(cls, value):
        return bleach.clean(value) # limpa o conteúdo HTML enviado pelo usuário (scripts, etc)

    # p garantir que a nota seja de 0 a 10
    @field_validator('rating')
    @classmethod
    def validar_nota(cls, value):
        if value < 0 or value > 10:
            raise ValueError('A nota deve estar entre 0 e 10')
        return value
