from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import pandas as pd

app = FastAPI()

# PostgreSQL connection settings
DB_CONFIG = {
    "host": "140.203.228.95",
    "port": 5432,
    "database": "sample_db",
    "user": "nocode_user",
    "password": "nocode_pass"
}

# Request body format
class QueryRequest(BaseModel):
    sql: str

@app.post("/run-sql")
def run_sql(request: QueryRequest):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        df = pd.read_sql_query(request.sql, conn)
        conn.close()
        return {"result": df.to_dict(orient="records")}
    except Exception as e:
        return {"error": str(e)}
