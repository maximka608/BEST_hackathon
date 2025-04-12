import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.database import engine, Base

def init_db():
    Base.metadata.create_all(bind=engine)
    print("INIT DB")

if __name__ == "__main__":
    init_db()