from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Artista(Base):
    __tablename__ = "artistas"

    id_artista = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    nascimento = Column(Integer)

    albuns = relationship("Album", back_populates="artista")

    def __repr__(self):
        return f"Artista: ID = {self.id_artista} | Nome = {self.nome} | Ano Nascimento = {self.nascimento}"
    
class Album(Base):
    __tablename__= "albuns"

    id_album =Column(Integer, primary_key=True, autoincrement=True)
    nome_album = Column(String(100), nullable=False)
    musicas = Column(Integer, nullable=False)
    estilo = Column(String(100))
    lancamento = Column(Integer, nullable=False)

    artista_id = Column(Integer, ForeignKey("artistas.id_artista"))

    artista = relationship("Artista", back_populates="albuns")


    def __repr__(self):
        return f"Álbum: ID = {self.id_album} | Nome = {self.nome_album} | Quantidade de Músicas = {self.musicas} | Estilo = {self.estilo} | Data de Lançamento = {self.lancamento}"
    
engine = create_engine("sqlite:///spotify.db")

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def adicionar_artista():
    nome_artista = input("Digite o nome do artista para adicionar: ")
    nascimento_artista = input("Digite a data de nascimento do artista: ")
    with Session() as session:
        try:
            artista = Artista(nome=nome_artista, nascimento= nascimento_artista)
            session.add(artista)
            session.commit()
            print("Artista adicionado!")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

# adicionar_artista()


