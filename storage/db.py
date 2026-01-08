from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import json

# Cria conexão com SQLite (arquivo states.db na raiz do projeto)
engine = create_engine("sqlite:///states.db", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# Modelo da tabela
class PageState(Base):
    __tablename__ = "page_states"
    page_id = Column(String, primary_key=True)
    state_json = Column(Text)

# Inicializa o banco e cria tabela se não existir
def init_db():
    Base.metadata.create_all(bind=engine)

# Recupera último estado salvo
def get_last_state(page_id):
    with SessionLocal() as session:
        obj = session.get(PageState, page_id)
        return json.loads(obj.state_json) if obj and obj.state_json else None

# Salva ou atualiza estado
def save_state(page_id, state_dict):
    with SessionLocal() as session:
        payload = json.dumps(state_dict, ensure_ascii=False)
        obj = session.get(PageState, page_id)
        if obj:
            obj.state_json = payload
        else:
            obj = PageState(page_id=page_id, state_json=payload)
            session.add(obj)
        session.commit()
