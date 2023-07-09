from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re

# Configurando a conexão com o banco de dados
engine = create_engine('Insira sua conexao com o banco de dados', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Definindo o modelo de Postagem
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content

# Definindo o modelo de Usuário
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

        if not self.validate_email():
            raise ValueError('Endereço de email invalido')

    def validate_email(self):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_regex, self.email)

# Criando as tabelas no banco de dados
Base.metadata.create_all(engine)

# Criando um usuário com e-mail inválido (para testar a validação)
try:
    user = User(name='Dominique toreto', email='dominique.toreto')
    session.add(user)
    session.commit()
except ValueError as e:
    print(f'Erro: {str(e)}')

# Criando um usuário válido
user = User(name='Thiago Ribeiro', email='thiagoribeiro@example.com')
session.add(user)
session.commit()

# Lendo os usuários do banco de dados
users = session.query(User).all()
for user in users:
    print(f'Nome: {user.name}')
    print(f'E-mail: {user.email}')
    print('---')
