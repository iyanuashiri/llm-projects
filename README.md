# llm-projects


## Check my blog
1. https://iyanuashiri.hashnode.dev/


## How to run migrations
1. install alembic
```
pip install alembic
```
2. Run the initial alembic
```
alembic init alembic
```
3. Configure alembic.ini file. Inside the file, scroll down until you see sqlalchemy.url variable. Update the variable. 
```python
sqlalchemy.url = sqlite:///commentiscan.db
```
4. Update the script.py.mako file
```python
import sqlmodel             # NEW

```
5. Update the env.py file by importing the SQLModel, the list of models, and the target_metadata
```python
from sqlmodel import SQLModel     # NEW

from app.models import User   # NEW

target_metadata = SQLModel.metadata             # UPDATED
```
6. Generate the migration
```python
alembic revision --autogenerate -m "Initial migration"   | Use this command

alembic revision -m "Initial migration"
```
7. Apply the migration 
```python
alembic upgrade head
```


1. https://fastapi.blog/blog/posts/2023-07-20-fastapi-sqlalchemy-migrations-guide/#step-6-generating-a-migration
1. https://alembic.sqlalchemy.org/en/latest/tutorial.html
1. https://testdriven.io/blog/fastapi-sqlmodel/
 