#uv run fastapi dev main.py
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc

Request comes in
Pydentic validates it (schemas.py)
SQL Alchemy (Stores or Retrieves the data)
Pydantic formats the response
Response goes out