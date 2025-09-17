from sqlmodel import SQLModel, create_engine
from sqlalchemy import event

DATABASE_URL = "sqlite:///./database.db"

# SQLite needs check_same_thread=False for multi-threaded FastAPI
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
)

# Ensure WAL mode and Foreign Keys on every connection
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

