from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

bd_URL = 'sqlite:///petshop.db'
engine = create_engine(bd_URL, echo=True)

Base = declarative_base()

# Cliente
class Cliente(Base):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    
    animais = relationship("Animal", back_populates="dono")

    def __repr__(self):
        return f"<Cliente(id={self.id}, nome='{self.nome}', email='{self.email}')>"

# Animal
class Animal(Base):
    __tablename__ = 'animais'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer)
    tipo = Column(String)
    id_dono = Column(Integer, ForeignKey('clientes.id'))
    
    dono = relationship("Cliente", back_populates="animais")

    def __repr__(self):
        return f"<Animal(id={self.id}, nome='{self.nome}', idade={self.idade}, tipo='{self.tipo}')>"
    
# Produto
class Produto(Base):
    __tablename__ = 'produtos'
    
    id_produto = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Produto(id_produto={self.id_produto}, nome='{self.nome}', preco='{self.preco}')>"


# Tabelas
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

#CRUD

#R-Read(ler)

def obter_clientes():
    clientes = session.query(Cliente).all()
    for cliente in clientes:
        print(cliente)

def obter_animais():
    animais = session.query(Animal).all()
    for animal in animais:
        print(animal)

def obter_produtos():
    produtos = session.query(Produto).all()
    for produto in produtos:
        print(produto)

#U-Uptade(atualizar)

def atualizar_cliente(id_cliente, nome=None, email=None):
    cliente = session.query(Cliente).filter_by(id=id_cliente).first()
    if cliente:
        if nome:
            cliente.nome = nome
        if email:
            cliente.email = email
        session.commit()
        print(f"Cliente atualizado: {cliente}")
    else:
        print("Cliente não encontrado")

def atualizar_animal(id_animal, nome=None, idade=None, tipo=None):
    animal = session.query(Animal).filter_by(id=id_animal).first()
    if animal:
        if nome:
            animal.nome = nome
        if idade:
            animal.idade = idade
        if tipo:
            animal.tipo = tipo
        session.commit()
        print(f"Animal atualizado: {animal}")
    else:
        print("Animal não encontrado")

def atualizar_produto(id_produto, nome=None, preco=None):
    produto = session.query(Produto).filter_by(id=id_produto).first()
    if produto:
        if nome:
            produto.nome = nome
        if preco:
            produto.preco = preco
        session.commit()
        print(f"Produto atualizado: {produto}")
    else:
        print("Produto não encontrado")

#D-Delete(deletar)

def deletar_cliente(id_cliente):
    cliente = session.query(Cliente).filter_by(id=id_cliente).first()
    if cliente:
        session.delete(cliente)
        session.commit()
        print(f"Cliente excluído: {cliente}")
    else:
        print("Cliente não encontrado")

def deletar_animal(id_animal):
    animal = session.query(Animal).filter_by(id=id_animal).first()
    if animal:
        session.delete(animal)
        session.commit()
        print(f"Animal excluído: {animal}")
    else:
        print("Animal não encontrado")

def deletar_produto(id_produto):
    produto = session.query(Produto).filter_by(id=id_produto).first()
    if produto:
        session.delete(produto)
        session.commit()
        print(f"Produto excluído: {produto}")
    else:
        print("Produto não encontrado")

#C-Criar

def adicionar_cliente(nome, email):
    novo_cliente = Cliente(nome=nome, email=email)
    session.add(novo_cliente)
    session.commit()

def adicionar_animal(nome, idade, tipo, id_dono):
    novo_animal = Animal(nome=nome, idade=idade, tipo=tipo, id_dono=id_dono)
    session.add(novo_animal)
    session.commit()

def adicionar_produto(nome, preco):
    novo_produto = Produto(nome=nome, preco=preco)
    session.add(novo_produto)
    session.commit()

if __name__ == "__main__":
    adicionar_cliente("Sophia Post", "sophia@exemplo.com")
    adicionar_cliente("Mariah Garcia", "mariah@exemplo.com")
    
    obter_clientes()
    
    sophia = session.query(Cliente).filter_by(nome="Sophia Post").first()
    mariah = session.query(Cliente).filter_by(nome="Mariah Garcia").first()

    adicionar_animal("Meg", 9, "Cachorro", sophia.id)
    adicionar_animal("Bucky", 3, "Gato", sophia.id)
    adicionar_animal("Hannah", 10, "Cachorro", mariah.id)
    adicionar_animal("Cuca", 7, "Cachorro", mariah.id)

    obter_animais()

    adicionar_produto("Ração para cachorros filhotes", 29.00)
    adicionar_produto("Petisco para Gato", 7.50)
    adicionar_produto("Casinha pequena", 32,90)
    
    obter_produtos()

