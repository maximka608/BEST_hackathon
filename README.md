# BEST_hackaton

run init_db.py to create your DB

run following command to init alembic:

```python
alembic init alembic
```

in alembic/env.py set your target_metadata as follows:
```python
from src.database import Base
target_metadata = Base.metadata
```

in alembic.ini change the connection string to your DB(run config.py to get your link)
```ini
sqlalchemy.url = sqlite:////...ACTUAL_LINK_TO_YOUR_DB
```

to create migrations run:
```python
alembic revision --autogenerate -m "Create tables"
```

to apply migrations run:
```python
alembic upgrade head
```