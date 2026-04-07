from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Artista(Base):
    __tablename__ = "artistas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    nascimento = Column(Integer)

    albuns = relationship("Album", back_populates="artista")

    def __repr__(self):
        return f"Artista: ID = {self.id} | Nome = {self.nome} | Ano Nascimento = {self.nascimento}"
    
class Album(Base):
    __tablename__= "albuns"

    id_album =Column(Integer, primary_key=True, autoincrement=True)
    nome_album = Column(String(100), nullable=False)
    musicas = Column(Integer, nullable=False)
    estilo = Column(String(100))
    lancamento = Column(Integer, nullable=False)

    artista_id = Column(Integer, ForeignKey("artistas.id"))

    artista = relationship("Artista", back_populates="albuns")


    def __repr__(self):
        return f"Álbum: ID = {self.id_album} | Nome = {self.nome_album} | Quantidade de Músicas = {self.musicas} | Estilo = {self.estilo} | Data de Lançamento = {self.lancamento}"
    
engine = create_engine("sqlite:///spotify.db")

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def adicionar_artista():
    nome_artista = input("Digite o nome do artista para adicionar: ").strip().capitalize()
    nascimento_artista = int(input("Digite a data de nascimento do artista: "))
    with Session() as session:
        try:
            artista = Artista(nome=nome_artista, nascimento= nascimento_artista)
            session.add(artista)
            session.commit()
            print(f"Artista {nome_artista} adicionado!")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

# adicionar_artista()

def adicionar_album():
    nome_album = input("Digite o nome do álbum: ").strip().capitalize()
    qtd_musicas = int(input("Digite a quantidade de músicas: "))
    estilo = input("Digite o estilo do álbum: ").capitalize()
    lancamento = int(input("Digite o ano de lançamento: "))
    buscar_artista = input(f"Digite o nome do artista do álbum {nome_album}: ").strip().capitalize()
    with Session() as session:
        try:
            artista = session.query(Artista).filter_by(nome=buscar_artista).first()
            if artista == None:
                print(f"Artista {buscar_artista} não encontrado!")
            else:
                album = Album(nome_album=nome_album, musicas=qtd_musicas, estilo=estilo, lancamento=lancamento,artista=artista)
                session.add(album)
                session.commit()
                print(f"Álbum {nome_album} adicionado com sucesso!")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

# adicionar_album()

def listar():
    with Session() as session:
        try:
            artistas = session.query(Artista).all()
            for i in artistas:
                print(f"\n{i}")
                for a in i.albuns:
                    print(a) 
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")
# listar()

def listar_artista():
    buscar_artista = input(f"Digite o nome do artista: ").strip().capitalize()
    with Session() as session:
        try:
            artista = session.query(Artista).filter_by(nome=buscar_artista).first()
            if artista == None:
                print(f"Artista {buscar_artista} não encontrado!")
            else:
                for i in artista.albuns:
                    print(f"\n{i}")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

# listar_artista()

def listar_validos():
    with Session() as session:
        try:
            artistas = session.query(Artista).filter(Artista.albuns != None).all()
            for i in artistas:
                print(f"\n{i}")
                for a in i.albuns:
                    print(a) 
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")
listar_validos()